#!/usr/bin/env python3
"""
Simple AI-based PR reviewer that summarizes diffs using OpenAI and posts a comment on the PR.

Requirements:
 - set repository secret `OPENAI_API_KEY`
 - optional secret `SLACK_WEBHOOK_URL` to receive notifications
 - workflow provides `TOKEN_GITHUB`, `REPO`, and `PR_NUMBER` env vars

This is a lightweight starter. Tweak prompts and output parsing for your needs.
"""
import os
import sys
import json
import requests
from github import Github
import importlib

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")
# Support either SLACK_WEBHOOK_URL or legacy SLACK_WEBHOOK
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL") or os.getenv("SLACK_WEBHOOK")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

if not ((GEMINI_API_KEY or OPENAI_API_KEY) and TOKEN_GITHUB and REPO and PR_NUMBER):
    print("Missing required environment variables. Exiting. Require GEMINI_API_KEY or OPENAI_API_KEY, TOKEN_GITHUB, REPO, and PR_NUMBER.")
    sys.exit(1)

def gather_diff(repo, pr_number):
    try:
        # PyGithub v2+ recommends using Auth.Token
        from github import Auth
        gh = Github(auth=Auth.Token(TOKEN_GITHUB))
    except Exception:
        # fall back to older constructor for older PyGithub versions
        gh = Github(TOKEN_GITHUB)
    repository = gh.get_repo(repo)
    pr = repository.get_pull(int(pr_number))
    files = pr.get_files()
    diffs = []
    for f in files:
        patch = f.patch or ""
        if patch:
            diffs.append(f"--- {f.filename}\n{patch}\n")
    return "\n\n".join(diffs), pr

def ask_gemini(prompt):
    """Prefer using the project's gemini client if available, otherwise call REST endpoint."""
    # Try to import the local gemini client from playwright/utils
    try:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        gemini_mod = importlib.import_module('playwright.utils.gemini_client')
        if hasattr(gemini_mod, 'ask_gemini'):
            return gemini_mod.ask_gemini(prompt)
    except Exception:
        # fallback to direct REST call below
        pass

    model = GEMINI_MODEL
    if model and not model.startswith("models/"):
        model = f"models/{model}"
    url = f"https://generativelanguage.googleapis.com/v1beta2/{model}:generateText?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "prompt": {"text": prompt},
        "temperature": 0.1,
        "maxOutputTokens": 1200,
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    j = resp.json()
    if isinstance(j, dict):
        if "candidates" in j and len(j["candidates"]) > 0 and "content" in j["candidates"][0]:
            return j["candidates"][0]["content"].strip()
        if "output" in j:
            out = j["output"]
            if isinstance(out, list) and len(out) > 0 and "content" in out[0]:
                return out[0]["content"].strip()
    return json.dumps(j)


def ask_openai(prompt):
    """Fallback to OpenAI if configured."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are an expert software engineer and security reviewer."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 1200,
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    resp.raise_for_status()
    j = resp.json()
    return j["choices"][0]["message"]["content"].strip()


def ask_ai(prompt):
    if GEMINI_API_KEY:
        return ask_gemini(prompt)
    if OPENAI_API_KEY:
        return ask_openai(prompt)
    raise RuntimeError("No AI API key configured (set GEMINI_API_KEY or OPENAI_API_KEY)")

def post_pr_comment(pr, body):
    pr.create_issue_comment(body)


def post_inline_comments(pr, review_text):
    """Post lightweight inline review comments on files mentioned in the AI review.
    For each file in the PR that is referenced by name in the review_text, add a
    single comment at the first added/changed line in the patch. This is best-effort
    and avoids creating noisy comments for files not mentioned by the AI output.
    """
    try:
        commits = list(pr.get_commits())
        if not commits:
            return
        last_sha = commits[-1].sha
        files = list(pr.get_files())
        comments = []
        for f in files:
            # Only comment on files that the AI review mentions
            if f.filename not in review_text:
                continue
            patch = f.patch or ""
            if not patch:
                continue
            # find first added line in the patch and use its position in the diff
            pos = None
            pos_counter = 0
            for ln in patch.splitlines():
                pos_counter += 1
                # skip file header lines like '+++'
                if ln.startswith('+++') or ln.startswith('---'):
                    continue
                if ln.startswith('+') and not ln.startswith('+++'):
                    pos = pos_counter
                    break
            if pos is None:
                continue
            body = (
                "Automated AI reviewer: the main review found a potential high-impact issue in this file.\n"
                "See the top-level AI review comment for details and remediation steps."
            )
            comments.append({
                'path': f.filename,
                'position': pos,
                'body': body,
            })

        if comments:
            # Create a single review containing all inline comments
            try:
                pr.create_review(body="Automated AI inline comments.", event="COMMENT", comments=comments)
            except Exception:
                # Older PyGithub versions may not accept 'comments' in create_review; fallback per-file
                for c in comments:
                    try:
                        pr.create_review_comment(c['body'], last_sha, c['path'], c['position'])
                    except Exception:
                        # give up on this file but continue
                        continue
    except Exception as e:
        print(f"Inline comment posting failed: {e}")

def post_slack_message(webhook, text):
    try:
        requests.post(webhook, json={"text": text}, timeout=10)
    except Exception as e:
        print(f"Slack notify failed: {e}")

def main():
    diffs, pr = gather_diff(REPO, PR_NUMBER)
    if not diffs:
        print("No patch/diff content found in PR.")
        return

    prompt = (
        "You are an expert software engineer and security reviewer. Review the git diff and RETURN ONLY the major, high-impact findings that affect security, correctness, reliability, or release readiness. Ignore stylistic, formatting, and minor style suggestions unless they cause correctness or security issues.\n\n"
        "Output requirements (strict):\n"
        "- Start with a prioritized list (max 3) of Critical/High issues.\n"
        "- For each finding include: Severity (Critical/High/Medium), one-line title, one-line description, 1-3 concrete remediation steps.\n"
        "- Provide minimal code snippets ONLY for Critical or High issues (show only the changed lines with filename and context).\n"
        "- Do NOT list low-impact or purely stylistic items.\n"
        "- Limit total output to ~800 words.\n\n"
        "Then, if any Medium issues exist, list them briefly under a separate heading.\n"
        "Finish with a one-line summary: either 'Ready to apply fixes' or 'No major issues found'.\n\n"
        "Diff:\n" + diffs
    )

    try:
        print("Requesting AI review from configured AI provider...")
        review_text = ask_ai(prompt)
    except Exception as e:
        review_text = f"AI review failed: {e}"

    comment_body = "## Automated AI Code Review\n\n" + review_text
    print(comment_body)
    print("Posting comment to PR...")
    post_pr_comment(pr, comment_body)

    # Post lightweight inline comments for any files the AI mentioned
    try:
        post_inline_comments(pr, review_text)
    except Exception as e:
        print(f"Posting inline comments failed: {e}")

    if SLACK_WEBHOOK:
        slack_text = f"AI Review posted for PR #{PR_NUMBER} in {REPO}:\n{review_text[:1500]}"
        post_slack_message(SLACK_WEBHOOK, slack_text)

    print("Done")

if __name__ == '__main__':
    main()
