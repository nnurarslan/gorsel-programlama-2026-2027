from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QCheckBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect

from ui.views.home_view import HomeView


# =========================
# CSS SPINNER
# =========================
class CssSpinner(QLabel):
    def __init__(self, size=26, parent=None):
        super().__init__(parent)

        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            QLabel {{
                border: 3px solid #1e293b;
                border-top: 3px solid #2563eb;
                border-radius: {size // 2}px;
                background: transparent;
            }}
        """)

        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(900)
        self._anim.setLoopCount(-1)

        self.hide()

    def start(self):
        self.show()
        rect = self.geometry()
        self._anim.setStartValue(rect)
        self._anim.setEndValue(rect)
        self._anim.start()

    def stop(self):
        self._anim.stop()
        self.hide()



class RegisterView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self._build_ui()
        self._bind_signals()

    def _build_ui(self):
        self.setWindowTitle("JurisAI – Register")
        self.setMinimumSize(360, 620)
        self.setStyleSheet(self._style_sheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)

        root.addStretch()

        # ===== CARD =====
        card = QFrame()
        card.setObjectName("Card")
        card.setMaximumWidth(420)
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(14)

        # Logo
        logo = QLabel("⚖️")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 32px;")
        layout.addWidget(logo)

        title = QLabel("Create your secure account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        layout.addWidget(title)

        subtitle = QLabel("Secure access for legal professionals.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("Subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(18)

        # Full Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Jane Doe")
        layout.addWidget(self._labeled("Full Name", self.name_input))

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("name@firm.com")
        layout.addWidget(self._labeled("Work Email", self.email_input))

        # Passwords
        pw_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("••••••")

        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setPlaceholderText("••••••")

        pw_layout.addWidget(self._labeled("Password", self.password_input))
        pw_layout.addWidget(self._labeled("Confirm", self.confirm_input))

        layout.addLayout(pw_layout)

        # Terms
        self.terms_checkbox = QCheckBox(
            "I agree to the Terms of Service & Privacy Policy.\n"
            "I confirm that I am an authorized legal practitioner."
        )
        self.terms_checkbox.setObjectName("Terms")
        layout.addWidget(self.terms_checkbox)

        # Register Button
        self.register_button = QPushButton("Register Account")
        self.register_button.setObjectName("PrimaryButton")
        layout.addWidget(self.register_button)

        # 🔄 SPINNER (BURASI ÖNEMLİ)
        self.spinner = CssSpinner(size=26)
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Error
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setObjectName("Error")
        layout.addWidget(self.error_label)

        # Login link
        login_link = QLabel("Already have an account? <a href='#'>Log in</a>")
        login_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_link.setTextFormat(Qt.TextFormat.RichText)
        login_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        layout.addWidget(login_link)

        root.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        root.addStretch()

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
        self.register_button.clicked.connect(self._on_register_clicked)

        self.view_model.loading_changed.connect(self._on_loading_changed)
        self.view_model.error.connect(self._on_error)
        self.view_model.register_success.connect(self._on_success)

    def _on_register_clicked(self):
        self.error_label.setText("")

        if self.password_input.text() != self.confirm_input.text():
            self.error_label.setText("Passwords do not match.")
            return

        if not self.terms_checkbox.isChecked():
            self.error_label.setText("You must accept the terms.")
            return

        self.view_model.register(
            self.name_input.text(),
            self.email_input.text(),
            self.password_input.text()
        )

    def _on_loading_changed(self, loading: bool):
        self.register_button.setDisabled(loading)

        if loading:
            self.spinner.start()
        else:
            self.spinner.stop()

    def _on_error(self, message: str):
        self.error_label.setText(message)

    def _on_success(self):
        self.error_label.setText("")
        print("REGISTER SUCCESS")


        self.main_view = HomeView()
        self.main_view.show()

        self.close()


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
            font-size: 20px;
            font-weight: 700;
        }

        #Subtitle {
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

        #PrimaryButton:hover {
            background-color: #1d4ed8;
        }

        #Error {
            color: #f87171;
            font-size: 11px;
        }

        #Terms {
            font-size: 11px;
            color: #94a3b8;
        }
        """
