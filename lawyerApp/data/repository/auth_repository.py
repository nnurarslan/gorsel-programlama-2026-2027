class AuthRepository:
    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, email, password):
        return self.api_client.post(
            "/api/auth/login",
            json_data={
                "email": email,
                "password": password
            },
            headers={
                "x-api-key": "E2pK0Yp0h87lQWlCDfsqMmWAQynTGOU7"
            }
        )

    def register(self, name, email, password):
        return self.api_client.post(
            "/api/auth/register",
            json_data={
                "name": name,
                "email": email,
                "password": password
            },
            headers={
                "x-api-key": "E2pK0Yp0h87lQWlCDfsqMmWAQynTGOU7"
            }
        )
