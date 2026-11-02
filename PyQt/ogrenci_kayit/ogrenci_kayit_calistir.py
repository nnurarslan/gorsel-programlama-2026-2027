import sys
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class OgrenciKayit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).with_name("ogrenci_kayit.ui")), self)
        self.btnKaydet.clicked.connect(self.kaydet)
        self.btnTemizle.clicked.connect(self.temizle)

    def kaydet(self):
        ad = self.txtAdSoyad.text().strip()
        no = self.txtOgrenciNo.text().strip()
        eposta = self.txtEposta.text().strip()
        bolum = self.cmbBolum.currentText()
        if not ad or not no or not eposta or self.cmbBolum.currentIndex() == 0:
            QMessageBox.warning(self, "Eksik bilgi", "Tüm alanları doldurun ve bölüm seçin.")
            return
        if not no.isdigit():
            QMessageBox.warning(self, "Hata", "Öğrenci numarası yalnızca rakamlardan oluşmalı.")
            return
        if not self.chkOnay.isChecked():
            QMessageBox.warning(self, "Onay", "Bilgileri onaylamalısınız.")
            return
        ogrenim = "İkinci öğretim" if self.rbIkinci.isChecked() else "Normal öğretim"
        self.lblDurum.setText(f"Hazır: {ad} ({no})")
        QMessageBox.information(self, "Örnek kayıt", f"{ad}\n{bolum}\n{ogrenim}\n{eposta}\n\nBu örnek veritabanına kayıt yapmaz.")

    def temizle(self):
        self.txtAdSoyad.clear()
        self.txtOgrenciNo.clear()
        self.txtEposta.clear()
        self.cmbBolum.setCurrentIndex(0)
        self.rbNormal.setChecked(True)
        self.chkOnay.setChecked(False)
        self.lblDurum.setText("Form temizlendi")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OgrenciKayit()
    window.show()
    sys.exit(app.exec_())
