from abc import ABC, abstractmethod
from application.dto.login_response_dto import LoginResponseDTO


class AuthRepository(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResponseDTO:
        pass
