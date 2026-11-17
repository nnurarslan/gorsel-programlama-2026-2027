from application.dto.law_category_dto import LawCategoryDTO
from data.api.api_client import ApiClient


class LawRepository:
    def __init__(self, api_client: ApiClient):
        self.api = api_client

    def get_law_categories(self):
        response = self.api.get(
            "/api/law-categories",
            headers={
                "x-api-key": "E2pK0Yp0h87lQWlCDfsqMmWAQynTGOU7"
            }
        )

        if response.get("status") != 200:
            return {
                "status": response.get("status"),
                "message": response.get("message", "Bilinmeyen hata")
            }

        categories = [
            LawCategoryDTO.from_json(item)
            for item in response.get("data", [])
        ]

        return {
            "status": 200,
            "data": categories
        }
