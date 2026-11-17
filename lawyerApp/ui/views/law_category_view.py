from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt

from application.dto.law_category_dto import LawCategoryDTO
from ui.viewmodels.law_category_viewmodel import LawCategoriesViewModel
from ui.views.register_view import CssSpinner


class LawCategoriesView(QWidget):
    def __init__(self, view_model: LawCategoriesViewModel):
        super().__init__()
        self.view_model = view_model

        self._build_ui()
        self._bind_signals()

        # Sayfa açılır açılmaz yükle
        self.view_model.load()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        self.setWindowTitle("Hukuk Kategorileri")
        self.setStyleSheet(self._style_sheet())

        # Minimum boyut ve başlangıç boyutu
        self.setMinimumSize(400, 600)
        self.resize(600, 700)  # Başlangıç boyutu

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Başlık
        title = QLabel("Hukuk Kategorileri")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(title)

        # Spinner
        self.spinner = CssSpinner(size=28)
        root.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        root.addWidget(self.scroll)

        # İç container
        self.container = QWidget()
        self.container.setMinimumWidth(500)
        self.container.setSizePolicy(
            self.container.sizePolicy().horizontalPolicy(),
            self.container.sizePolicy().verticalPolicy()
        )

        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setSpacing(12)
        self.scroll.setWidget(self.container)

    # =========================
    # Signals
    # =========================
    def _bind_signals(self):
        self.view_model.loading_changed.connect(self._on_loading)
        self.view_model.data_loaded.connect(self._render_list)
        self.view_model.error.connect(self._on_error)

    # =========================
    # State handlers
    # =========================
    def _on_loading(self, loading: bool):
        if loading:
            self.spinner.start()
        else:
            self.spinner.stop()

    def _render_list(self, categories: list[LawCategoryDTO]):
        # Önce temizle
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for category in categories:
            self.list_layout.addWidget(
                self._category_card(category)
            )

        self.list_layout.addStretch()

    def _on_error(self, message: str):
        error = QLabel(message)
        error.setObjectName("Error")
        self.list_layout.addWidget(error)

    # =========================
    # Components
    # =========================
    def _category_card(self, category: LawCategoryDTO) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        name = QLabel(category.name)
        name.setObjectName("CardTitle")

        desc = QLabel(category.description)
        desc.setWordWrap(True)
        desc.setObjectName("CardDescription")

        layout.addWidget(name)
        layout.addWidget(desc)

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

        #Card {
            background-color: #0f172a;
            border-radius: 14px;
            padding: 14px;
        }

        #CardTitle {
            font-size: 14px;
            font-weight: 600;
        }

        #CardDescription {
            font-size: 12px;
            color: #94a3b8;
        }

        #Error {
            color: #f87171;
            font-size: 12px;
        }
        """
