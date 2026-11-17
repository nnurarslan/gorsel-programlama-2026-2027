from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from core.session.session_manager import SessionManager
from data.api.api_client import ApiClient
from data.repository.law_asistant_repository import LawAssistantRepository
from data.repository.law_repository import LawRepository
from application.use_cases.law_category_use_case import LawCategoryUseCase
from ui.viewmodels.law_category_viewmodel import LawCategoriesViewModel
from data.repository.auth_repository import AuthRepository
from application.use_cases.login_user_use_case import LoginUserUseCase
from ui.viewmodels.login_viewmodel import LoginViewModel


class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JurisAI – Main")
        self.setMinimumSize(400, 500)
        self.setStyleSheet(self._style_sheet())

        self._api_client = ApiClient()

        user = SessionManager.user()

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        # Başlık
        title = QLabel(f"Hoşgeldin {user['name']}")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        # Spacer
        root.addStretch()

        # Buttons container
        btn_container = QVBoxLayout()
        btn_container.setSpacing(16)

        btn_laws = QPushButton("Hukuk Kategorileri")
        btn_laws.setObjectName("PrimaryButton")
        btn_container.addWidget(btn_laws)

        btn_assistant = QPushButton("Hukuk Asistanı")
        btn_assistant.setObjectName("PrimaryButton")
        btn_container.addWidget(btn_assistant)

        btn_logout = QPushButton("Çıkış Yap")
        btn_logout.setObjectName("SecondaryButton")
        btn_container.addWidget(btn_logout)

        # Butonları root layout'a ekle
        btn_frame = QFrame()
        btn_frame.setLayout(btn_container)
        btn_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        root.addWidget(btn_frame)

        # Spacer
        root.addStretch()

        # Buton sinyalleri
        btn_laws.clicked.connect(self._open_law_categories)
        btn_assistant.clicked.connect(self._open_law_assistant)
        btn_logout.clicked.connect(self._logout)

    # =========================
    # Navigation
    # =========================
    def _open_law_categories(self):
        from ui.views.law_category_view import LawCategoriesView

        repo = LawRepository(self._api_client)
        use_case = LawCategoryUseCase(repo)
        vm = LawCategoriesViewModel(use_case)

        self.law_view = LawCategoriesView(vm)
        self.law_view.show()

    def _open_law_assistant(self):
        # Local import ile circular import önleniyor
        from ui.views.law_asistant_view import LawAssistantView
        from application.use_cases.law_asistant_use_case import LawAssistantUseCase
        from data.repository.law_repository import LawRepository
        from data.api.api_client import ApiClient
        from ui.viewmodels.law_asistant_viewmodel import LawAssistantViewModel

        api_client = ApiClient()
        repo = LawAssistantRepository(api_client)
        use_case = LawAssistantUseCase(repo)
        vm = LawAssistantViewModel(use_case)

        self.assistant_view = LawAssistantView(vm)
        self.assistant_view.show()

    def _logout(self):
        from ui.views.login_view import LoginView

        SessionManager.clear()

        api_client = ApiClient()
        auth_repo = AuthRepository(api_client)
        login_use_case = LoginUserUseCase(auth_repo)
        login_vm = LoginViewModel(login_use_case)

        self.login_view = LoginView(login_vm)
        self.login_view.show()

        self.close()

    # =========================
    # Styles
    # =========================
    def _style_sheet(self):
        return """
        QWidget {
            background-color: #0b1220;
            color: #e5e7eb;
            font-family: Arial, sans-serif;
        }

        #Title {
            font-size: 22px;
            font-weight: 700;
            color: #e5e7eb;
        }

        QPushButton {
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            min-width: 200px;
        }

        #PrimaryButton {
            background-color: #2563eb;
            color: #ffffff;
        }

        #PrimaryButton:hover {
            background-color: #1d4ed8;
        }

        #SecondaryButton {
            background-color: #1e293b;
            color: #94a3b8;
        }

        #SecondaryButton:hover {
            background-color: #334155;
        }
        """
