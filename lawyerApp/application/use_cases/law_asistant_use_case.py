from data.repository.law_asistant_repository import LawAssistantRepository


class LawAssistantUseCase:
    def __init__(self, repository: LawAssistantRepository):
        self.repository = repository

    def execute(self, question: str, law_category_id: int, token: str):
        return self.repository.ask_question(question, law_category_id)
