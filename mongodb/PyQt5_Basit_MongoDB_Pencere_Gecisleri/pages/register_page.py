from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from pymongo.errors import DuplicateKeyError, PyMongoError
from database import users

UI_DIR = Path(__file__).resolve().parent.parent / "ui"


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_DIR / "register.ui"), self)
        self.btnCreate.clicked.connect(self.register)
        self.btnBack.clicked.connect(self.back)

    def register(self):
        first = self.txtFirstName.text().strip()
        last = self.txtLastName.text().strip()
        email = self.txtEmail.text().strip().lower()
        password = self.txtPassword.text()
        confirm = self.txtConfirm.text()
        if not first or not last or not email or not password:
            QMessageBox.warning(self, "Eksik Bilgi", "Bütün alanları doldurunuz.")
            return
        if "@" not in email:
            QMessageBox.warning(self, "Hata", "E-posta adresini kontrol ediniz.")
            return
        if password != confirm:
            QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor.")
            return
        try:
            users.insert_one({
                "first_name": first,
                "last_name": last,
                "email": email,
                "password": password,
            })
        except DuplicateKeyError:
            QMessageBox.warning(self, "Kayıt Hatası", "Bu e-posta zaten kayıtlı.")
            return
        except PyMongoError as error:
            QMessageBox.critical(self, "MongoDB Hatası", str(error))
            return
        QMessageBox.information(self, "Başarılı", "Kullanıcı MongoDB'ye kaydedildi.")
        self.back()

    def back(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
