from PyQt6.QtWidgets import QStackedWidget, QWidget


class AppRouter(QStackedWidget):
    def __init__(self):
        super().__init__()
        self._routes: dict[str, QWidget] = {}

    def register(self, name: str, widget: QWidget):
        """
        Yeni bir sayfayı router'a ekler.
        """
        if name in self._routes:
            return  # Aynı isimle tekrar ekleme

        self._routes[name] = widget
        self.addWidget(widget)

    def go(self, name: str):
        """
        Kayıtlı bir sayfaya geçiş yapar.
        """
        widget = self._routes.get(name)
        if not widget:
            raise ValueError(f"Route '{name}' bulunamadı")

        self.setCurrentWidget(widget)
