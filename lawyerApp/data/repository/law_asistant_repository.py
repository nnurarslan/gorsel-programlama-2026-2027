from data.api.api_client import ApiClient
from application.dto.law_asistant_dto import LawAssistantResponseDTO
from core.session.session_manager import SessionManager


class LawAssistantRepository:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def ask_question(self, question: str, law_category_id: int) -> LawAssistantResponseDTO:
        token = SessionManager.access_token()  # token'ı SessionManager'dan al

        response = self.api_client.post(
            "/api/law-assistant/ask",
            json_data={
                "question": question,
                "lawCategoryId": law_category_id,
                "tone": "formal"
            },
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-key": "E2pK0Yp0h87lQWlCDfsqMmWAQynTGOU7",
                "x-device-id": "test-cihaz-1",
                "Content-Type": "application/json"
            }
        )

        # Artık response zaten dict
        if response.get("status") != 200:
            raise Exception(response.get("message", "Bilinmeyen hata"))

        return LawAssistantResponseDTO.from_json(response.get("data", {}))
