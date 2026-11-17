from core.session.session_manager import SessionManager


class LoginUserUseCase:
    def __init__(self, auth_repository):
        self.auth_repository = auth_repository

    def execute(self, email, password, remember):
        response = self.auth_repository.login(email, password)

        if response.get("status") != 200:
            raise Exception(response.get("message", "Login failed"))

        data = response["data"]

        SessionManager.set_session(
            access_token=data["accessToken"],
            refresh_token=data["refreshToken"],
            user=data["user"]
        )

        # remember == True ise buraya kalıcı kayıt eklenir (sonra)

        return True
