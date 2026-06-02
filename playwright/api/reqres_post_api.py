import allure

class ReqresPostApi(object):

    def __init__(self, page, api_key):
        self.request = page.request
        self.api_key = api_key

    def reqres_post_api(self):
        payload = {
            "name": "Rohith Nandakumar",
            "job": "QA Automation Architect"
        }

        response = self.request.post(
            "https://reqres.in/api/users",
            headers={
                "x-api-key": self.api_key
            },
            data=payload
        )

        assert response.status == 201
        json_response = response.json()
        print(json_response)
        assert json_response["name"] == "Rohith Nandakumar"
        assert json_response["job"] == "QA Automation Architect"