import requests

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer your_token_here"
}

response = requests.get("https://example.api/yourext", headers=headers)

assert response.status_code == 200
print("Response code:", response.status_code)

assert response.json()["process_id"] == "1234"
print("Process id:", response.json()["process_id"])

payload = {
    "id": "1234",
    "name": "Rohith Nandakumar"
}

response = requests.post("https://example.api/yourext", headers=headers, json=payload)

print(response.status_code == 201)
print(response.json()["message"])



