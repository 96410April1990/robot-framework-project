import json

def extract_value_from_json():
    json_data = '''
    {
        "person": {
            "name": {
                "first": "John",
                "last": "Doe"
            },
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "CA"
            }
        }
    }
    ''' 
    
    data = json.loads(json_data)
    first_name = data['person']['name']['first']
    print(f"First Name: {first_name}")
    return first_name

if __name__ == "__main__":
    extract_value_from_json()