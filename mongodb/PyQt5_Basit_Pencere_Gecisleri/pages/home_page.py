from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

UI_DIR = Path(__file__).resolve().parent.parent / "ui"

class HomePage(QWidget):
    def __init__(self, email=""):
        super().__init__()
        uic.loadUi(str(UI_DIR / "home.ui"), self)
        self.lblInfo.setText("Hoş geldiniz: " + email)
        self.btnLogout.clicked.connect(self.logout)

    def logout(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
