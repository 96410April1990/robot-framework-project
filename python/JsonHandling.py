import json

data = {
    "name": "Rohith Nandakumar",
    "age": 36,
    "city": "Chennai"
}

json_data = json.dumps(data)
print(json_data)

parsed_json_data = json.loads(json_data)
print(parsed_json_data["name"])
print(parsed_json_data["age"])
print(parsed_json_data["city"])