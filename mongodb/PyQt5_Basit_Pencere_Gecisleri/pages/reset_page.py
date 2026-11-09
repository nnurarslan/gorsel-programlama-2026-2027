from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

UI_DIR = Path(__file__).resolve().parent.parent / "ui"

class ResetPage(QWidget):
    def __init__(self, email=""):
        super().__init__()
        uic.loadUi(str(UI_DIR / "reset.ui"), self)
        self.txtEmail.setText(email)
        self.btnReset.clicked.connect(self.reset_password)
        self.btnBack.clicked.connect(self.back)

    def reset_password(self):
        if not self.txtEmail.text().strip() or not self.txtRecovery.text().strip():
            QMessageBox.warning(self, "Eksik Bilgi", "E-posta ve kurtarma kodu giriniz.")
            return
        if not self.txtNewPassword.text() or self.txtNewPassword.text() != self.txtConfirm.text():
            QMessageBox.warning(self, "Hata", "Yeni şifreler boş veya eşleşmiyor.")
            return
        QMessageBox.information(self, "Demo", "Form kontrol edildi. Henüz şifre güncellenmedi.")
        self.back()

    def back(self):
        from pages.login_page import LoginPage
        self.next_window = LoginPage()
        self.next_window.show()
        self.close()
