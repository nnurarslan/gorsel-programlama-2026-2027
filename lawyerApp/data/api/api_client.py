import requests


class ApiClient:
    BASE_URL = "http://localhost:3000"

    def get(self, path, headers=None, params=None):
        url = f"{self.BASE_URL}{path}"
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=100
        )

        if not response.ok:
            raise Exception(response.text)

        return response.json()

    def post(self, path, json_data=None, headers=None):
        url = f"{self.BASE_URL}{path}"
        response = requests.post(
            url,
            json=json_data,
            headers=headers,
            timeout=100
        )

        if not response.ok:
            raise Exception(response.text)

        return response.json()
