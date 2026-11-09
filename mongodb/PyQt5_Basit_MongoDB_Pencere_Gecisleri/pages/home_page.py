from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

UI_DIR = Path(__file__).resolve().parent.parent / "ui"


class HomePage(QWidget):
    def __init__(self, first_name="", last_name=""):
        super().__init__()
        uic.loadUi(str(UI_DIR / "home.ui"), self)
        self.lblInfo.setText(f"Hoş geldiniz, {first_name} {last_name}!")
        self.btnLogout.clicked.connect(self.logout)

    def logout(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
