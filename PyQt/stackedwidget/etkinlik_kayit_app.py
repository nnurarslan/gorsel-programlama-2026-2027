"""Qt Designer .ui dosyasından üretilen sınıfla çalışan örnek."""
import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_etkinlik_kayit import Ui_MainWindow


class EtkinlikKayit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dateEtkinlik.setDate(QDate.currentDate())
        self.ui.dateEtkinlik.setMinimumDate(QDate.currentDate())
        self.ui.btnGeri.clicked.connect(self.geri)
        self.ui.btnIleri.clicked.connect(self.ileri)
        self.ui.btnTamam.clicked.connect(self.tamamla)
        self.ui.stackedWidget.currentChanged.connect(self.adimi_guncelle)
        self.adimi_guncelle(0)

    def adimi_guncelle(self, indeks):
        basliklar = ["Katılımcı Bilgileri", "Tercihler", "Tarih ve Saat", "Özet"]
        self.ui.lblAdim.setText(f"Adım {indeks + 1} / 4 — {basliklar[indeks]}")
        self.ui.btnGeri.setEnabled(indeks > 0)
        self.ui.btnIleri.setVisible(indeks < 3)
        self.ui.btnTamam.setVisible(indeks == 3)
        if indeks == 3:
            self.ozet_olustur()

    def ilk_sayfa_gecerli_mi(self):
        ad = self.ui.txtAdSoyad.text().strip()
        eposta = self.ui.txtEposta.text().strip()
        if not ad or "@" not in eposta or "." not in eposta.split("@")[-1]:
            QMessageBox.warning(self, "Eksik Bilgi",
                                "Ad soyad ve geçerli bir e-posta adresi giriniz.")
            return False
        return True

    def ileri(self):
        indeks = self.ui.stackedWidget.currentIndex()
        if indeks == 0 and not self.ilk_sayfa_gecerli_mi():
            return
        if indeks == 1 and not self.secili_atolyeler():
            QMessageBox.warning(self, "Atölye Seçimi",
                                "En az bir atölye seçiniz.")
            return
        if indeks < self.ui.stackedWidget.count() - 1:
            self.ui.stackedWidget.setCurrentIndex(indeks + 1)

    def geri(self):
        indeks = self.ui.stackedWidget.currentIndex()
        if indeks > 0:
            self.ui.stackedWidget.setCurrentIndex(indeks - 1)

    def secili_atolyeler(self):
        secimler = [
            (self.ui.chkPython, "Python ile Veri Analizi"),
            (self.ui.chkQt, "PyQt Arayüz Tasarımı"),
            (self.ui.chkYapayZeka, "Yapay Zekâ Uygulamaları"),
        ]
        return [ad for kutu, ad in secimler if kutu.isChecked()]

    def ozet_olustur(self):
        katilim = "Yüz yüze" if self.ui.rbYuzYuze.isChecked() else "Çevrim içi"
        satirlar = [
            f"Ad Soyad: {self.ui.txtAdSoyad.text().strip()}",
            f"E-posta: {self.ui.txtEposta.text().strip()}",
            f"Bölüm: {self.ui.cmbBolum.currentText()}",
            f"Katılım: {katilim}",
            f"Atölyeler: {', '.join(self.secili_atolyeler())}",
            f"Tarih: {self.ui.dateEtkinlik.date().toString('dd.MM.yyyy')}",
            f"Saat: {self.ui.timeEtkinlik.time().toString('HH:mm')}",
            f"Not: {self.ui.txtNot.toPlainText().strip() or '-'}",
        ]
        self.ui.txtOzet.setPlainText("\n".join(satirlar))

    def tamamla(self):
        QMessageBox.information(self, "Başarılı",
                                "Örnek kayıt tamamlandı. Veriler kalıcı olarak kaydedilmedi.")
        self.statusBar().showMessage("Kayıt işlemi örnek olarak tamamlandı.", 5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = EtkinlikKayit()
    pencere.show()
    sys.exit(app.exec_())
