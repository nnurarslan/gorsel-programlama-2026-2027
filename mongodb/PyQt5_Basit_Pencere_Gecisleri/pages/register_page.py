from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

UI_DIR = Path(__file__).resolve().parent.parent / "ui"

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_DIR / "register.ui"), self)
        self.btnCreate.clicked.connect(self.register)
        self.btnBack.clicked.connect(self.back)

    def register(self):
        if not all([self.txtFirstName.text().strip(), self.txtLastName.text().strip(), self.txtEmail.text().strip(), self.txtPassword.text()]):
            QMessageBox.warning(self, "Eksik Bilgi", "Bütün alanları doldurunuz.")
            return
        if self.txtPassword.text() != self.txtConfirm.text():
            QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor.")
            return
        QMessageBox.information(self, "Demo", "Form kontrol edildi. Henüz veritabanına kayıt yapılmadı.")
        self.back()

    def back(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
