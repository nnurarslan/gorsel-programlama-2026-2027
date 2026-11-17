import sys

from PyQt6.QtWidgets import QApplication

from application.use_cases.law_category_use_case import LawCategoryUseCase
from data.api.api_client import ApiClient
from data.repository.law_repository import LawRepository
from ui.viewmodels.law_category_viewmodel import LawCategoriesViewModel
from ui.views.law_category_view import LawCategoriesView


def main():
    app = QApplication(sys.argv)

    api_client = ApiClient()
    law_category_repository = LawRepository(api_client)
    law_category_use_case = LawCategoryUseCase(law_category_repository)
    law_category_vm = LawCategoriesViewModel(law_category_use_case)
    law_category_view = LawCategoriesView(law_category_vm)
    law_category_view.show()



    sys.exit(app.exec())



if __name__ == "__main__":
    main()
