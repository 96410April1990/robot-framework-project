import requests

def a_simple_api_call():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        if "title" in json_data:
            print("Title available in the JSON response: " + json_data["title"])
        else:
            print("Title not found in the JSON response")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


a_simple_api_call()