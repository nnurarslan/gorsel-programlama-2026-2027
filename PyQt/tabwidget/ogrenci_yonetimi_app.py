import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget,
    QVBoxLayout, QLabel, QTableWidgetItem
)
from ui_ogrenci_yonetimi import Ui_MainWindow


class OgrenciYonetimi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.yeni_sekme_sayaci = 0

        self.ui.btnKaydet.clicked.connect(self.kaydet)
        self.ui.btnTemizle.clicked.connect(self.temizle)
        self.ui.btnYeniSekme.clicked.connect(self.yeni_sekme)
        self.ui.btnSekmeKapat.clicked.connect(self.sekme_kapat)
        self.ui.tabWidget.currentChanged.connect(self.aktif_sekmeyi_guncelle)
        self.aktif_sekmeyi_guncelle(self.ui.tabWidget.currentIndex())

    def kaydet(self):
        ad = self.ui.txtAd.text().strip()
        soyad = self.ui.txtSoyad.text().strip()
        bolum = self.ui.cmbBolum.currentText()

        if not ad or not soyad:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad ve soyad giriniz.")
            return

        tablo = self.ui.tblOgrenciler
        satir = tablo.rowCount()
        tablo.insertRow(satir)
        for sutun, deger in enumerate((ad, soyad, bolum)):
            tablo.setItem(satir, sutun, QTableWidgetItem(deger))

        self.temizle()
        self.ui.tabWidget.setCurrentIndex(1)

    def temizle(self):
        self.ui.txtAd.clear()
        self.ui.txtSoyad.clear()
        self.ui.cmbBolum.setCurrentIndex(0)
        self.ui.txtAd.setFocus()

    def yeni_sekme(self):
        self.yeni_sekme_sayaci += 1
        sayfa = QWidget()
        layout = QVBoxLayout(sayfa)
        layout.addWidget(QLabel(
            f"Dinamik oluşturulan sekme {self.yeni_sekme_sayaci}"
        ))
        indeks = self.ui.tabWidget.addTab(
            sayfa, f"Yeni Sekme {self.yeni_sekme_sayaci}"
        )
        self.ui.tabWidget.setCurrentIndex(indeks)

    def sekme_kapat(self):
        indeks = self.ui.tabWidget.currentIndex()
        if indeks < 3:
            QMessageBox.information(
                self, "Bilgi", "İlk üç temel sekme kapatılamaz."
            )
            return
        self.ui.tabWidget.removeTab(indeks)

    def aktif_sekmeyi_guncelle(self, indeks):
        print(indeks)
        if indeks >= 0:
            baslik = self.ui.tabWidget.tabText(indeks)
            self.ui.lblAktifSekme.setText(
                f"Aktif sekme: {indeks} - {baslik}"
            )
        else:
            self.ui.lblAktifSekme.setText("Aktif sekme: yok")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = OgrenciYonetimi()
    pencere.show()
    sys.exit(app.exec_())
