import json

def read_json():

    bioData = {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "Java", "JavaScript"]
    }

    name = bioData["name"]
    age = bioData["age"]
    skills = bioData["skills"]

    print(name)
    print(age)

    for skill in skills:
        print(skill)

read_json()

