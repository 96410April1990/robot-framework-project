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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
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
    """Call Google Generative Language (Gemini) REST endpoint using API key.
    This expects `GEMINI_API_KEY` and `GEMINI_MODEL` to be set.
    """
    model = GEMINI_MODEL
    # Normalize model to resource path if needed (e.g., 'gemini-1.5-flash' -> 'models/gemini-1.5-flash')
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
    # Response shape may vary; try common patterns
    if isinstance(j, dict):
        # text-bison style
        if "candidates" in j and len(j["candidates"]) > 0 and "content" in j["candidates"][0]:
            return j["candidates"][0]["content"].strip()
        # some APIs return 'output' with 'content'
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
        "Review the following git diff and provide:\n"
        "1) Brief summary of potential coding-style / standards issues.\n"
        "2) Security or correctness concerns and suggested fixes.\n"
        "3) Concrete code suggestions (show the minimal corrected snippet where applicable).\n\n"
        "Diff:\n" + diffs
    )

    try:
        print("Requesting AI review from configured AI provider...")
        review_text = ask_ai(prompt)
    except Exception as e:
        review_text = f"AI review failed: {e}"

    comment_body = "## Automated AI Code Review\n\n" + review_text
    print("Posting comment to PR...")
    post_pr_comment(pr, comment_body)

    if SLACK_WEBHOOK:
        slack_text = f"AI Review posted for PR #{PR_NUMBER} in {REPO}:\n{review_text[:1500]}"
        post_slack_message(SLACK_WEBHOOK, slack_text)

    print("Done")

if __name__ == '__main__':
    main()
