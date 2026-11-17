from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from core.session.session_manager import SessionManager
from ui.views.register_view import CssSpinner
from application.dto.law_asistant_dto import LawAssistantResponseDTO
from ui.viewmodels.law_asistant_viewmodel import LawAssistantViewModel
import json


class LawAssistantView(QWidget):
    def __init__(self, view_model: LawAssistantViewModel):
        super().__init__()
        self.view_model = view_model

        # Token artık SessionManager'dan alınıyor
        user_raw = SessionManager.user()
        if isinstance(user_raw, str):
            try:
                user = json.loads(user_raw)
            except json.JSONDecodeError:
                user = {}
        else:
            user = user_raw

        self.token = user.get("accessToken", "")

        self._build_ui()
        self._bind_signals()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        self.setWindowTitle("Hukuk Asistanı")
        self.setMinimumSize(600, 700)
        self.setStyleSheet(self._style_sheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(12)

        title = QLabel("Hukuk Asistanı")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        self.spinner = CssSpinner(size=28)
        root.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        root.addWidget(self.scroll)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setSpacing(12)
        self.scroll.setWidget(self.container)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Sorunuzu buraya yazın...")
        self.question_input.setObjectName("QuestionInput")

        self.send_button = QPushButton("Gönder")
        self.send_button.setObjectName("PrimaryButton")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.question_input)
        input_layout.addWidget(self.send_button)
        root.addLayout(input_layout)

    # =========================
    # Signals
    # =========================
    def _bind_signals(self):
        self.send_button.clicked.connect(self._on_send)
        self.view_model.loading_changed.connect(self._on_loading)
        self.view_model.response_loaded.connect(self._render_response)
        self.view_model.error.connect(self._on_error)

    # =========================
    # Handlers
    # =========================
    def _on_send(self):
        question = self.question_input.text().strip()
        if not question:
            return
        # Varsayılan Ceza Kanunu
        self.view_model.ask_question(question, law_category_id=3)
        self.question_input.clear()

    def _on_loading(self, loading: bool):
        if loading:
            self.spinner.start()
        else:
            self.spinner.stop()

    def _render_response(self, data: LawAssistantResponseDTO):
        # Temizle
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Kullanıcı sorusu
        self.list_layout.addWidget(self._message_card(data.question, user=True))

        # API cevabı
        self.list_layout.addWidget(self._message_card(data.answer, user=False))

        # İlgili kanun maddeleri
        if data.related_articles:
            label = QLabel("İlgili Kanun Maddeleri")
            label.setObjectName("SectionTitle")
            self.list_layout.addWidget(label)

            for article in data.related_articles:
                card = QFrame()
                card.setObjectName("Card")
                layout = QVBoxLayout(card)
                layout.setSpacing(4)

                # Burada dict yerine DTO attribute kullan
                num = QLabel(f"MADDE {article.article_number}")
                num.setObjectName("CardTitle")
                content = QLabel(article.content)
                content.setWordWrap(True)
                content.setObjectName("CardDescription")

                layout.addWidget(num)
                layout.addWidget(content)

                self.list_layout.addWidget(card)

        self.list_layout.addStretch()
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def _on_error(self, message: str):
        self.list_layout.addWidget(QLabel(f"Hata: {message}"))

    # =========================
    # Components
    # =========================
    def _message_card(self, text: str, user: bool) -> QFrame:
        card = QFrame()
        card.setObjectName("UserCard" if user else "BotCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        return card

    # =========================
    # Style
    # =========================
    def _style_sheet(self):
        return """
        QWidget {
            background-color: #0b1220;
            color: #e5e7eb;
        }

        #Title {
            font-size: 20px;
            font-weight: 700;
        }

        #QuestionInput {
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
            color: #e5e7eb;
        }

        #PrimaryButton {
            background-color: #2563eb;
            border-radius: 10px;
            padding: 10px;
            font-weight: 600;
        }

        #PrimaryButton:hover {
            background-color: #1d4ed8;
        }

        #UserCard {
            background-color: #1e293b;
            border-radius: 10px;
            padding: 8px;
        }

        #BotCard {
            background-color: #0f172a;
            border-radius: 10px;
            padding: 8px;
        }

        #Card {
            background-color: #0f172a;
            border-radius: 14px;
            padding: 12px;
        }

        #CardTitle {
            font-size: 13px;
            font-weight: 600;
        }

        #CardDescription {
            font-size: 12px;
            color: #94a3b8;
        }

        #SectionTitle {
            font-size: 14px;
            font-weight: 700;
            margin-top: 10px;
        }
        """
