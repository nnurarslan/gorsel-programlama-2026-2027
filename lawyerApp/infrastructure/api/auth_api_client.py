import requests


class AuthApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def login(self, email: str, password: str) -> dict:
        url = f"{self.base_url}/api/auth/login"

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            raise Exception(response.json().get("message", "Login failed"))

        print(response.json())

        return response.json()
