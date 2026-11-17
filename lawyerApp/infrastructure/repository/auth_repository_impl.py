from core.interfaces.auth_repository import AuthRepository
from application.dto.login_response_dto import LoginResponseDTO


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, email: str, password: str) -> LoginResponseDTO:
        data = self.api_client.login(email, password)

        return LoginResponseDTO(
            access_token=data.get("accessToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=data.get("expiresIn")
        )
