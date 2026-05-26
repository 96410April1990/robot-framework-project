import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "required": ["id", "name", "salary"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "salary": {"type": "number"}
    }
}

valid_json = {
    "id": 1234,
    "name": "Rohith",
    "salary": 75000
}

invalid_json = {
    "id": "abcd",
    "name": 1234,
    "salary": "75000"
}

try:
    validate(instance=valid_json, schema=schema)
    print("valid_data: Schema validation passed")
except jsonschema.ValidationError as e:
    print(f"valid_data: Schema validation error {e.message}")

try:
    validate(instance=invalid_json, schema=schema)
    print("invalid_data: Schema validation passed")
except jsonschema.ValidationError as e:
    print(f"invalid_data: Schema validation error {e.message}")