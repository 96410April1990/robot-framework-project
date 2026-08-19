import os
import json
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


def ask_gemini(prompt: str) -> str:
    """
    Robust Gemini caller:
    - Prefer the new `google.genai` client if installed.
    - Fallback to the legacy `google.generativeai` if present.
    - Otherwise use the REST endpoint via `requests`.
    """
    # Try new google.genai client
    try:
        from google import genai
        try:
            client = genai.Client()
            resp = client.generate_text(model=GEMINI_MODEL, prompt=prompt)
            # many client versions expose `text` or `content`
            return getattr(resp, "text", getattr(resp, "content", str(resp)))
        except TypeError:
            # some versions accept different args
            resp = genai.generate_text(model=GEMINI_MODEL, input=prompt)
            return resp.text if hasattr(resp, 'text') else str(resp)
    except Exception:
        pass

    # Try legacy google.generativeai
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return getattr(response, "text", str(response))
    except Exception:
        pass

    # Fallback to REST call
    try:
        import requests
        model = GEMINI_MODEL
        if model and not model.startswith("models/"):
            model = f"models/{model}"
        url = f"https://generativelanguage.googleapis.com/v1beta2/{model}:generateText?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"prompt": {"text": prompt}, "temperature": 0.1, "maxOutputTokens": 1200}
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        resp.raise_for_status()
        j = resp.json()
        if isinstance(j, dict):
            if "candidates" in j and len(j["candidates"]) > 0:
                return j["candidates"][0].get("content") or j["candidates"][0].get("text", "")
            if "output" in j:
                out = j["output"]
                if isinstance(out, list) and len(out) > 0 and "content" in out[0]:
                    return out[0]["content"]
        return str(j)
    except Exception as e:
        raise RuntimeError(f"All Gemini call methods failed: {e}")
