from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QCheckBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie

from ui.views.home_view import HomeView


class LoginView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self._build_ui()
        self._bind_signals()

    def _build_ui(self):
        self.setWindowTitle("JurisAI – Login")
        self.setMinimumSize(360, 520)
        self.setStyleSheet(self._style_sheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)

        root.addStretch()

        # ===== CARD =====
        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.card.setMaximumWidth(420)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(32, 32, 32, 32)

        # Logo
        logo = QLabel("⚖️")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 32px;")
        card_layout.addWidget(logo)

        title = QLabel("JurisAI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        card_layout.addWidget(title)

        subtitle = QLabel("LEGAL ASSISTANT WORKSPACE")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("Subtitle")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(12)

        welcome = QLabel("Welcome Back")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setObjectName("Welcome")
        card_layout.addWidget(welcome)

        desc = QLabel("Please sign in to access your cases.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setObjectName("Description")
        card_layout.addWidget(desc)

        card_layout.addSpacing(18)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        card_layout.addWidget(self._labeled("Email Address", self.email_input))

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self._labeled("Password", self.password_input))

        # Remember / Forgot
        options = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")

        forgot = QLabel("<a href='#'>Forgot Password?</a>")
        forgot.setTextFormat(Qt.TextFormat.RichText)
        forgot.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        forgot.setAlignment(Qt.AlignmentFlag.AlignRight)

        options.addWidget(self.remember_checkbox)
        options.addStretch()
        options.addWidget(forgot)

        card_layout.addLayout(options)

        # Login Button
        self.login_button = QPushButton("Log In")
        self.login_button.setObjectName("PrimaryButton")
        card_layout.addWidget(self.login_button)

        # Loading Animation
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()

        self.spinner = QMovie("ui/resources/spinner.gif")
       # self.spinner.setScaledSize(Qt. (24, 24))
        self.loading_label.setMovie(self.spinner)
        card_layout.addWidget(self.loading_label)

        # Error
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setObjectName("Error")
        card_layout.addWidget(self.error_label)

        root.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)
        root.addStretch()

        # ===== LOADING OVERLAY =====
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("""
            background-color: rgba(11, 18, 32, 180);
        """)
        self.overlay.hide()

        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.overlay_spinner_label = QLabel()
        self.overlay_spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.overlay_spinner = QMovie("ui/resources/spinner.gif")
        self.overlay_spinner_label.setMovie(self.overlay_spinner)

        overlay_layout.addWidget(self.overlay_spinner_label)


    def _labeled(self, text, widget):
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setObjectName("InputLabel")
        layout.addWidget(label)
        layout.addWidget(widget)

        container = QWidget()
        container.setLayout(layout)
        return container

    def _bind_signals(self):
        # UI → ViewModel
        self.login_button.clicked.connect(self._on_login_clicked)

        # ViewModel → UI
        self.view_model.loading_changed.connect(self._set_loading)
        self.view_model.login_success.connect(self._on_login_success)
        self.view_model.error.connect(self._on_error)

    def _on_login_clicked(self):
        self.error_label.setText("")
        self.view_model.login(
            self.email_input.text(),
            self.password_input.text(),
            self.remember_checkbox.isChecked()
        )

    def _set_loading(self, is_loading: bool):
        self.login_button.setDisabled(is_loading)
        self.email_input.setDisabled(is_loading)
        self.password_input.setDisabled(is_loading)
        self.remember_checkbox.setDisabled(is_loading)

        if is_loading:
            self.overlay.show()
            self.overlay_spinner.start()
        else:
            self.overlay_spinner.stop()
            self.overlay.hide()

    def _on_login_success(self):
        print("Login başarılı → HomeView")
        self.home_view = HomeView()
        self.home_view.show()
        self.close()  # Login penceresini kapat

    def _on_error(self, message: str):
        self.error_label.setText(message)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.rect())


    def _style_sheet(self):
        return """
        QWidget {
            background-color: #0b1220;
            color: #e5e7eb;
        }

        #Card {
            background-color: #0f172a;
            border-radius: 16px;
        }

        #Title {
            font-size: 22px;
            font-weight: 700;
        }

        #Subtitle {
            font-size: 10px;
            color: #94a3b8;
            letter-spacing: 1px;
        }

        #Welcome {
            font-size: 18px;
            font-weight: 600;
        }

        #Description {
            font-size: 12px;
            color: #94a3b8;
        }

        #InputLabel {
            font-size: 11px;
            color: #cbd5f5;
        }

        QLineEdit {
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 10px;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
        }

        #PrimaryButton {
            background-color: #2563eb;
            border-radius: 10px;
            padding: 12px;
            font-weight: 600;
        }

        #PrimaryButton:disabled {
            background-color: #1e40af;
        }

        #Error {
            color: #f87171;
            font-size: 11px;
        }
        """


