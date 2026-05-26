import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import base64

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://dctech-request-explorer.qa.ca.walmart.com/requestexplorer/v1/privacyrequest/file/download"

headers = {
    "Content-Type":"application/json",
    "Authorization": "Bearer Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InIwbjAxZ3UiLCJzYWlscG9pbnREYXRhIjp7InJvbGVzIjpbeyJyb2xlQ29kZSI6IkRDU1BfQURNSU4iLCJyb2xlTmFtZSI6IkRDU1AtQWRtaW4iLCJyb2xlRGVzY3JpcHRpb24iOiJOb3JtYWwgVXNlciBmb3IgRENTUCdzIERvY3VtZW50IFJlZGFjdGlvbiJ9LHsicm9sZUNvZGUiOiJEUk0tUkVWSUVXRVIiLCJyb2xlTmFtZSI6IkRDU1AgRFJNIHJldmlld2VyIiwicm9sZURlc2NyaXB0aW9uIjoiUmV2aWV3ZXIgcm9sZSBmb3IgRENTUCdzIERSTSBhcHBsaWNhdGlvbiJ9XX0sInVzZXJEYXRhIjp7ImZpcnN0TmFtZSI6Ik4gUm9oaXRoIiwibGFzdE5hbWUiOiIuIiwiZW1haWwiOiJyb2hpdGgubmFuZGFrdW1hckB3YWxtYXJ0LmNvbSIsImxkYXBJZCI6InIwbjAxZ3UiLCJhZEdyb3VwcyI6WyJkYy1jYS1xYS1jdXN0b21lci1yZXAiLCJkYy1jYS1xYS1qb2JhcHBsaWNhbnQtcmVwIiwiZGMtY2EtcWEtc3VwcGxpZXItcmVwIiwiZGMtY2EtcWEtYXNzb2NpYXRlLXJlcCJdfSwicmVzb3VyY2VzIjpbeyJyZXNvdXJjZVR5cGUiOiJhc3NldCIsInJlc291cmNlVmFsdWUiOltdfV0sImV4cCI6MTcxMjA3Nzg3NCwiaWF0IjoxNzEyMDQ5MDc0fQ.BerLt9NnAaPHmyAybTtGoJyIIrYidxqKtwrspRKsiLg",
    "Cookie": "JSESSIONID=2246C89D8219DE1A91310E362682526C",
    "WM_CONSUMER.ID": "7b91a295-8932-4811-9b35-c1fb388d9544",
    "WM_SVC.NAME": "DCTECH-REQUEST-EXPLORER-SERVICE-APP",
    "WM_SVC.ENV": "stg:7.0.0"
}

data = {
    "id": "090ceafc-6df0-4b31-b8ba-e84aa1a8f7b9"
}

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

if response.status_code == 200:
    #response_body_bytes = response.content
    #response_body_text = response_body_bytes.decode('ISO-8859-1')
    with open("Downloads/"+"090ceafc-6df0-4b31-b8ba-e84aa1a8f7b9.pdf", "wb") as file:
        print(response.content)
        #text = response.content.decode('ISO-8859-1')
        #print(text)
        print(response.status_code)
        file.write(response.content)
        #file.write(text)
else:
    print(f"Request failed with status code {response.status_code}")

