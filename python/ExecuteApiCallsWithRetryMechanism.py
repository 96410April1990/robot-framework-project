import requests
import time 

BASE_URL = "https://api.example.com/"
MAX_RETRIES = 3
RETRY_DELAY = 2

def call_api_with_retry(url, payload, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        print(f"Attempt {attempt} of {max_retries} to call API...")

        try:
            response = requests.post(url, json=payload)
            
            if response.status_code != 201:
                print(f" Failed: Expected 201, got {response.status_code}")
                raise ValueError(f"Bad status code: {response.status_code}")
            
            body = response.json()
            if "status" not in body or "processId" not in body:
                raise ValueError(f"Missing fields in response: {body}")
            
            if "successfully" not in body:
                raise ValueError(f"Unexpected status message: {body}")
            
            print(f"Success: {body}")
            return body
        
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError) as e:
            print(f"Network error: {e}")

        except ValueError as e:
            print(f"Validation error: {e}")

        if attempt < max_retries:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    raise Exception(f"API call failed after {max_retries} attempts")