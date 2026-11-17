from dataclasses import dataclass


@dataclass(frozen=True)
class LawCategoryDTO:
    id: int
    name: str
    description: str

    @staticmethod
    def from_json(json: dict) -> "LawCategoryDTO":
        return LawCategoryDTO(
            id=json.get("id"),
            name=json.get("name"),
            description=json.get("description")
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
