import requests

json_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
}

if "name" in json_data:
    print("Name available in the JSON response"+' '+json_data["name"])
else:
    print("Name not found in the JSON response")