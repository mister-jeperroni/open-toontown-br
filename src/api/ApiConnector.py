import requests


class ApiConnector:
    def __init__(self, api_url=None):
        self.api_url = "http://127.0.0.1:3000/api/"
        self.api_endpoints = {
            "validate_token": "auth/validate-token",
            "login": "auth/login",
        }
        if api_url:
            self.api_url = api_url

    def validate_token(self, playToken):
        try:
            response = requests.post(
                self.api_url + self.api_endpoints["validate_token"],
                json={"token": playToken},
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def authorize(self, username, password):
        try:
            response = requests.post(
                self.api_url + self.api_endpoints["login"],
                json={"username": username, "password": password},
            )
            response.raise_for_status()
            return {"success": True, "token": response.json().get("token")}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
