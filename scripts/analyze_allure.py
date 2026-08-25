#!/usr/bin/env python3
"""
Lightweight Allure analyzer agent.

Scans an `allure-results` directory (or multiple past result dirs) and produces:
- summary counts (passed/failed/skipped)
- list of failing tests with extracted failure messages
- heuristic classification of likely cause (application / test / infra / unknown)
- simple flakiness metric when history dirs are provided

Usage:
  python scripts/analyze_allure.py --results-dir playwright/allure-results \
      --history-dir previous_run_1/allure-results --history-dir previous_run_2/allure-results

Optional environment variables:
  SLACK_WEBHOOK_URL  - if set, a short summary will be posted to Slack
  GITHUB_TOKEN       - if set, the script can be extended to post a PR comment

This script is intentionally conservative and heuristic-based; treat classifications
as suggestions to triage, not definitive root-cause analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
import time
import importlib

try:
    import requests
except Exception:
    requests = None

# AI configuration (Gemini preferred, OpenAI fallback)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.5-flash')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def ask_gemini(prompt: str) -> str:
    # Try local gemini client first (playwright/utils/gemini_client.py)
    try:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        gemini_mod = importlib.import_module('playwright.utils.gemini_client')
        if hasattr(gemini_mod, 'ask_gemini'):
            return gemini_mod.ask_gemini(prompt)
    except Exception:
        pass

    if not GEMINI_API_KEY:
        raise RuntimeError('GEMINI_API_KEY not configured')

    model = GEMINI_MODEL
    if model.startswith('models/'):
        model = model.replace('models/', '')

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 1200}
    }

    if not requests:
        raise RuntimeError('requests library required for Gemini REST call')

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response is not None else 'Unknown'
        raise RuntimeError(f'Gemini API request failed with status code: {status_code}')

    j = resp.json()
    try:
        if 'candidates' in j and len(j['candidates']) > 0:
            first_candidate = j['candidates'][0]
            content_node = first_candidate.get('content', {})
            parts = content_node.get('parts', [])
            if len(parts) > 0 and 'text' in parts[0]:
                return parts[0]['text'].strip()
    except Exception:
        pass
    return json.dumps(j)

def ask_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not configured')
    if not requests:
        raise RuntimeError('requests library required for OpenAI call')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    data = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'You are an expert test engineer and root-cause analyst.'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.0,
        'max_tokens': 1200,
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    j = resp.json()
    return j['choices'][0]['message']['content'].strip()

def ask_ai(prompt: str) -> str:
    # Prefer Gemini, fallback to OpenAI
    try:
        if GEMINI_API_KEY:
            return ask_gemini(prompt)
    except Exception as e:
        # don't leak keys; surface only the error type
        print(f'Gemini call failed: {e}')
    if OPENAI_API_KEY:
        return ask_openai(prompt)
    raise RuntimeError('No AI provider configured (set GEMINI_API_KEY or OPENAI_API_KEY)')

def _redact_text_secrets(text: str) -> str:
    if not isinstance(text, str):
        return text
    redacted = text
    # Generic API key / token style patterns in free text
    redacted = re.sub(r'(?i)(api[_-]?key\s*[=:]\s*)([^\s,;]+)', r'\1***REDACTED***', redacted)
    redacted = re.sub(r'(?i)(authorization\s*:\s*bearer\s+)([^\s,;]+)', r'\1***REDACTED***', redacted)
    redacted = re.sub(r'(?i)(token\s*[=:]\s*)([^\s,;]+)', r'\1***REDACTED***', redacted)
    # Gemini key format commonly starts with AIza
    redacted = re.sub(r'AIza[0-9A-Za-z\-_]{20,}', '***REDACTED***', redacted)
    return redacted

def _sanitize_for_output(value):
    sensitive_key_markers = ('password', 'secret', 'token', 'api_key', 'apikey', 'authorization', 'key')
    if isinstance(value, dict):
        sanitized = {}
        for k, v in value.items():
            key_lower = str(k).lower()
            if any(marker in key_lower for marker in sensitive_key_markers):
                sanitized[k] = '***REDACTED***'
            else:
                sanitized[k] = _sanitize_for_output(v)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_for_output(v) for v in value]
    if isinstance(value, str):
        return _redact_text_secrets(value)
    return value

def ask_ai_for_failure(name: str, message: str, history: List[str]) -> Dict[str, object]:
    """Ask the AI to classify a single failure and provide remediation suggestions."""
    prompt = (
        f"Analyze the following failing test and return a JSON object with keys:\n"
        f"- classification: one of application, test, infra, flaky\n"
        f"- confidence: float 0..1\n"
        f"- suggestion: short remediation steps\n\n"
        f"Test: {name}\n"
        f"Failure message:\n{message}\n\n"
        f"Recent history (most recent first): {history}\n\n"
        "Respond ONLY with valid JSON."
    )
    try:
        res = ask_ai(prompt)
        # Try to parse JSON
        parsed = json.loads(res)
        return parsed
    except Exception:
        # Fallback to heuristic classification
        cls, conf = classify_failure(message)
        return {'classification': cls, 'confidence': conf, 'suggestion': 'No AI suggestion available.'}

def ask_ai_for_analysis(summary: Dict) -> str:
    """Ask the AI to analyze the whole summary and return actionable recommendations."""
    prompt_lines = [
        "You are an expert SDET and reliability engineer. Review the following test run summary and provide:",
        "1) Overall root-cause analysis of why tests failed (application/test/infra).",
        "2) Concrete remediation actions for developers and test authors.",
        "3) Prioritized checklist to reduce flakiness and improve stability.",
        "Respond in markdown." ,
        "\nSummary:\n",
    ]
    prompt_lines.append(json.dumps(summary, indent=2))
    prompt = '\n'.join(prompt_lines)
    try:
        analysis = ask_ai(prompt)
        return analysis
    except Exception as e:
        print(f'AI analysis failed: {e}')
        return 'AI analysis unavailable.'


def find_result_jsons(results_dir: str) -> List[str]:
    files = []
    for root, _, filenames in os.walk(results_dir):
        for fn in filenames:
            if fn.endswith('.json'):
                path = os.path.join(root, fn)
                files.append(path)
    return files


def parse_allure_result(path: str) -> Optional[Dict]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def extract_test_info(j: Dict) -> Optional[Dict]:
    # Allure result JSONs vary; tests often contain 'name', 'status', 'fullName', 'statusDetails'
    if not isinstance(j, dict):
        return None
    name = j.get('name') or j.get('title')
    status = j.get('status')
    full_name = j.get('fullName') or j.get('historyId') or name
    details = j.get('statusDetails') or {}
    message = None
    if isinstance(details, dict):
        message = details.get('message') or details.get('trace')
    # some frameworks embed failure in 'steps' or 'attachments'
    if not message:
        # look for 'steps' with failures
        steps = j.get('steps') or []
        for s in steps:
            sd = s.get('statusDetails') or {}
            if sd.get('message'):
                message = sd.get('message')
                break
    return {'name': name, 'status': status, 'fullName': full_name, 'message': message}


def classify_failure(message: Optional[str]) -> Tuple[str, float]:
    """Return (classification, confidence)

    classifications: application, test, infra, unknown
    """
    if not message:
        return 'unknown', 0.2
    m = message.lower()
    # heuristics
    if 'assert' in m or 'assertion' in m or 'expected' in m and 'but was' in m:
        return 'application', 0.7
    if 'timeout' in m or 'timed out' in m or 'timeouterror' in m:
        return 'test/infra-flaky', 0.6
    if 'no such element' in m or 'locator' in m or 'element not found' in m or 'not visible' in m:
        return 'application-or-test-locator', 0.5
    if 'connection refused' in m or 'connection reset' in m or 'econnrefused' in m or 'networkerror' in m:
        return 'infra', 0.7
    if 'selenium' in m or 'playwright' in m or 'driver' in m:
        return 'test', 0.6
    # generic stacktrace present
    if re.search(r'\bexception\b|\berror\b', m):
        return 'unknown', 0.4
    return 'unknown', 0.2


def analyze_results(results_dir: str) -> Tuple[Counter, List[Dict]]:
    files = find_result_jsons(results_dir)
    counts = Counter()
    failures = []
    for p in files:
        j = parse_allure_result(p)
        if not j:
            continue
        info = extract_test_info(j)
        if not info:
            continue
        status = (info.get('status') or 'unknown').lower()
        counts[status] += 1
        if status in ('failed', 'broken', 'failed'):  # include 'broken'
            failures.append({'path': p, **info})
    return counts, failures


def aggregate_history(history_dirs: List[str]) -> Dict[str, List[str]]:
    """Return mapping fullName -> list of statuses across history dirs (most recent first)"""
    agg = defaultdict(list)
    for d in history_dirs:
        files = find_result_jsons(d)
        for p in files:
            j = parse_allure_result(p)
            if not j:
                continue
            info = extract_test_info(j)
            if not info:
                continue
            agg[info['fullName']].append((info['status'] or 'unknown').lower())
    return agg


def score_flakiness(statuses: List[str]) -> float:
    # simple metric: fraction of runs that differ from the most common status
    if not statuses:
        return 0.0
    c = Counter(statuses)
    most_common = c.most_common(1)[0][1]
    n = len(statuses)
    return 1.0 - (most_common / n)


def render_summary(counts: Counter, failures: List[Dict], history_map: Dict[str, List[str]]) -> Dict:
    total = sum(counts.values())
    passed = counts.get('passed', 0)
    failed = counts.get('failed', 0) + counts.get('broken', 0)
    skipped = counts.get('skipped', 0)
    unstable_rate = None
    if total:
        unstable_rate = (failed / total) * 100.0

    items = []
    for f in failures:
        msg = f.get('message') or ''
        cls, conf = classify_failure(msg)
        history = history_map.get(f['fullName'], [])
        flakiness = score_flakiness(history) if history else 0.0
        items.append({
            'name': f.get('name'),
            'fullName': f.get('fullName'),
            'message': msg,
            'classification': cls,
            'confidence': conf,
            'history': history,
            'flakiness': flakiness,
            'source_file': f.get('path')
        })

    summary = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'total_tests': total,
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'unstable_rate_percent': unstable_rate,
        'failures': items,
    }
    return summary

def post_to_slack(webhook: str, summary: Dict) -> None:
    if not requests:
        print('requests not available; skipping Slack post')
        return
    text_lines = [f"Allure analysis at {summary['timestamp']}", f"Total: {summary['total_tests']}, Failed: {summary['failed']}, Unstable%: {summary['unstable_rate_percent']:.1f}%"]
    top = summary['failures'][:5]
    if top:
        text_lines.append('\nTop failures:')
        for t in top:
            text_lines.append(f"- {t['name']} -> {t['classification']} ({t['confidence']:.2f})")
    payload = {'text': '\n'.join(text_lines)}
    try:
        # Include AI insights (truncated) if present
        ai_insights = summary.get('ai_insights') if isinstance(summary, dict) else None
        if ai_insights:
            # keep message reasonably short for Slack
            snippet = ai_insights if len(ai_insights) <= 1500 else ai_insights[:1497] + '...'
            payload['text'] = payload['text'] + '\n\nAI insights:\n' + snippet
        r = requests.post(webhook, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print('Slack post failed:', e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-dir', default='playwright/allure-results', help='Path to latest allure-results')
    parser.add_argument('--history-dir', action='append', default=[], help='Path to previous allure-results directories (repeatable)')
    parser.add_argument('--output-json', help='Write summary JSON to this file')
    parser.add_argument('--post-slack', action='store_true', help='Post short summary to SLACK_WEBHOOK_URL env var')
    args = parser.parse_args()

    counts, failures = analyze_results(args.results_dir)
    history_map = aggregate_history(args.history_dir) if args.history_dir else {}
    summary = render_summary(counts, failures, history_map)
    # If AI provider configured, enrich each failure with AI classification/suggestion
    if GEMINI_API_KEY or OPENAI_API_KEY:
        for f in summary.get('failures', []):
            try:
                ai_resp = ask_ai_for_failure(f.get('name') or f.get('fullName'), f.get('message', ''), f.get('history', []))
                if isinstance(ai_resp, dict):
                    f['ai_classification'] = ai_resp.get('classification')
                    f['ai_confidence'] = float(ai_resp.get('confidence') or 0)
                    f['ai_suggestion'] = ai_resp.get('suggestion')
            except Exception as e:
                print(f'AI per-failure call failed: {e}')
        # Get overall AI analysis (markdown)
        try:
            summary['ai_insights'] = ask_ai_for_analysis(summary)
        except Exception as e:
            print(f'AI overall analysis failed: {e}')

    #out = json.dumps(summary, indent=2)
    safe_summary = _sanitize_for_output(summary)
    out = json.dumps(safe_summary, indent=2)

    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            f.write(out)

    if args.post_slack:
        slack = os.getenv('SLACK_WEBHOOK_URL')
        if slack:
            post_to_slack(slack, summary)
        else:
            print('SLACK_WEBHOOK_URL not set; skipping Slack post')


if __name__ == '__main__':
    main()
