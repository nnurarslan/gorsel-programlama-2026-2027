from dataclasses import dataclass


@dataclass
class LoginResponseDTO:
    access_token: str
    refresh_token: str | None
    expires_in: int | None
