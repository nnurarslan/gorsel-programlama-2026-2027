import sys
from PyQt6.QtWidgets import QApplication

from application.use_cases.register_user_use_case import RegisterUserUseCase
from ui.views.login_view import LoginView
from ui.viewmodels.login_viewmodel import LoginViewModel
from ui.viewmodels.register_viewmodel import RegisterViewModel

from application.use_cases.login_user_use_case import LoginUserUseCase
from data.repository.auth_repository import AuthRepository
from data.api.api_client import ApiClient
from ui.views.register_view import RegisterView


def main():
    app = QApplication(sys.argv)


    # Dependency wiring
    api_client = ApiClient()
    auth_repo = AuthRepository(api_client)
    login_use_case = LoginUserUseCase(auth_repo)
    register_use_case = RegisterUserUseCase(auth_repo)
    register_vm = RegisterViewModel(register_use_case)
    login_vm = LoginViewModel(login_use_case)

    login_view = LoginView(login_vm)
    login_view.show()
    register_view = RegisterView(register_vm)
   # register_view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
