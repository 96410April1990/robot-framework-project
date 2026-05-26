import json

name = "Rohith"
nameReverse = name[::-1]
print("Reversed String:", nameReverse)

original_json = {"Name": "Rohith", "Age": 30, "City": "New York"}
reversed_json = {value: key for key, value in original_json.items()}

print("Original JSON:", original_json)
print("Reversed JSON:", reversed_json)