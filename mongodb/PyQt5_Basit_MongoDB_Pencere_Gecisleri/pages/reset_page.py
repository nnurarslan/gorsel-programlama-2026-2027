from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from pymongo.errors import PyMongoError
from database import users

UI_DIR = Path(__file__).resolve().parent.parent / "ui"


class ResetPage(QWidget):
    def __init__(self, email=""):
        super().__init__()
        uic.loadUi(str(UI_DIR / "reset.ui"), self)
        self.txtEmail.setText(email)
        self.btnReset.clicked.connect(self.reset_password)
        self.btnBack.clicked.connect(self.back)

    def reset_password(self):
        email = self.txtEmail.text().strip().lower()
        recovery = self.txtRecovery.text().strip()
        new_password = self.txtNewPassword.text()
        confirm = self.txtConfirm.text()
        if not email or not recovery or not new_password:
            QMessageBox.warning(self, "Eksik Bilgi", "Bütün alanları doldurunuz.")
            return
        if new_password != confirm:
            QMessageBox.warning(self, "Hata", "Yeni şifreler eşleşmiyor.")
            return
        try:
            # İlk derste kurtarma kodu sistemi yok: kayıtlı mevcut şifre istenir.
            result = users.update_one(
                {"email": email, "password": recovery},
                {"$set": {"password": new_password}}
            )
        except PyMongoError as error:
            QMessageBox.critical(self, "MongoDB Hatası", str(error))
            return
        if result.matched_count == 0:
            QMessageBox.warning(self, "Hata", "E-posta veya mevcut şifre yanlış.")
            return
        QMessageBox.information(self, "Başarılı", "Şifre güncellendi.")
        self.back()

    def back(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
