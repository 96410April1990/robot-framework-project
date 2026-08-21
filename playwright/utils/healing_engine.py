import json

from utils.gemini_client import ask_gemini
from utils.dom_parser import get_dom_summary

PAGE_CACHE = {}

def generate_locators(page, failed_locator, action):
    title = page.title()
    url = page.url

    dom = get_dom_summary(page)

    prompt = f"""
    You are an expert Playwright automation engineer.

    A web element action has failed.

    Action: {action}

    Failed locator: {failed_locator}

    Page title: {title}

    URL: {url}

    DOM summary: {json.dumps(dom, indent=2)}

    Generate possible replacement locators.

    Rules:

    1. Return only JSON.
    2. Give multiple locator strategies.
    3. Prefer:
       id
       data-testid
       aria-label
       text
       css
       xpath or dynamic xpath

    Output format:

    [
     {{
         "locator":"#example",
         "type":"css",
         "confidence":0.95
     }}
    ]

    """

    result = ask_gemini(prompt)

    cleaned_result = result.replace("```json","").replace("```","")

    return json.loads(cleaned_result)

def execute_action(page, locator, action, **kwargs):
    element = page.locator(locator)
    if action == "click":
        element.click(timeout=5000)
    elif action == "input_text":
        element.fill(kwargs["text"], timeout=5000)
    elif action == "get_text":
        return element.text_content()
    elif action == "clear_text":
        element.fill("")    
    elif action == "is_visible":
        element.wait_for(state="visible", timeout=5000)
        return True
    elif action == "wait_for_element":
        element.wait_for(timeout=5000)
        return True
    elif action == "hover":
        element.hover(timeout=5000)
    elif action == "select_option":
        element.select_option(**kwargs)
    elif action == "file_upload":
        element.set_input_files(kwargs["file_path"])
    elif action == "drag_and_drop":
        element.drag_to(page.locator(kwargs["target_locator"]), timeout=5000)

def heal_and_execute(page, locator, action, **kwargs):
    try:
        return execute_action(page, locator, action, **kwargs)
    except Exception:
        print(f"Original web element locator failed: {locator}")
        page_key = page.url
        if page_key not in PAGE_CACHE:
            PAGE_CACHE[page_key] = generate_locators(page, locator, action)
        print(PAGE_CACHE[page_key])
        candidates = PAGE_CACHE[page_key]
        for item in candidates:
            new_locator=item["locator"]
            confidence=item.get("confidence", 0)
            if confidence < 0.75:
                continue
            try:
                print("Trying AI locator:", new_locator)
                return execute_action(page, new_locator, action, **kwargs)
            except Exception:
                continue
    raise Exception("AI healing failed. Kindly update the locator manually.")
