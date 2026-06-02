import allure

class ReqresGetApi(object):

    def __init__(self, page, api_key):
        self.request = page.request
        self.api_key = api_key

    def reqres_get_api(self):
        response = self.request.get(
            "https://reqres.in/api/users/2",
            headers={
                "x-api-key": self.api_key
            }
        )

        assert response.status == 200
        json_response = response.json()
        print(json_response)
        assert json_response["data"]["id"] == 2
        assert json_response["data"]["email"] == "janet.weaver@reqres.in"
        assert json_response["data"]["first_name"] == "Janet"
        assert json_response["data"]["last_name"] == "Weaver"