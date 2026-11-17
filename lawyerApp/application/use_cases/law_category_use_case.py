class LawCategoryUseCase:
    def __init__(self, law_repository):
        self.law_repository = law_repository

    def execute(self):
        response = self.law_repository.get_law_categories()

        if response.get("status") != 200:
            raise Exception(
                response.get("message", "Kategoriler alınamadı")
            )

        data = response.get("data", [])

        return data
