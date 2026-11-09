from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

UI_DIR = Path(__file__).resolve().parent.parent / "ui"

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_DIR / "login.ui"), self)
        self.btnRegister.clicked.connect(self.open_register)
        self.btnForgot.clicked.connect(self.open_reset)
        self.btnLogin.clicked.connect(self.login)

    def open_register(self):
        from pages.register_page import RegisterPage
        self.next_window = RegisterPage()
        self.next_window.show()
        self.close()

    def open_reset(self):
        from pages.reset_page import ResetPage
        self.next_window = ResetPage(self.txtEmail.text())
        self.next_window.show()
        self.close()

    def login(self):
        if not self.txtEmail.text().strip() or not self.txtPassword.text():
            QMessageBox.warning(self, "Eksik Bilgi", "E-posta ve şifre giriniz.")
            return
        # Eğitim aşaması: henüz gerçek kullanıcı doğrulaması yok.
        from pages.home_page import HomePage
        self.next_window = HomePage(self.txtEmail.text().strip())
        self.next_window.show()
        self.close()
