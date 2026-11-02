"""QListWidget örneği: Kitap listesi.

1) Arayüzü Python dosyasına dönüştür:
   python -m PyQt5.uic.pyuic kitap_listwidget.ui -o ui_kitap_listwidget.py
2) Uygulamayı çalıştır:
   python kitap_listwidget.py

NOT: Bu örnekte uic.loadUi() KULLANILMAZ.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# Qt Designer'ın .ui dosyasından ürettiğimiz Python sınıfını içe aktarıyoruz.
# Bu dosya, yukarıdaki dönüştürme komutuyla oluşur.
from ui_kitap_listwidget import Ui_MainWindow


class KitapPenceresi(QMainWindow, Ui_MainWindow):
    """Ana pencere sınıfı: QMainWindow ve üretilmiş arayüz sınıfını miras alır."""

    def __init__(self):
        super().__init__()

        # Designer'da çizilen widget'ları bu pencere üzerinde oluşturur.
        # Artık self.txtKitap, self.listKitaplar gibi nesnelere erişebiliriz.
        self.setupUi(self)

        # QListWidget, QListView'dan farklı olarak ayrı bir
        # QStringListModel oluşturulmasını GEREKTİRMEZ.
        # addItems() ile başlangıç kitaplarını doğrudan ekliyoruz.
        self.listKitaplar.addItems(["Python Temelleri", "Algoritmalar"])

        # Butonların clicked sinyalini ilgili fonksiyonlara bağlıyoruz.
        self.btnEkle.clicked.connect(self.ekle)
        self.btnSil.clicked.connect(self.sil)
        self.btnTemizle.clicked.connect(self.temizle)

        # Kullanıcı kitap adını yazıp Enter'a basarsa da ekleme yapılır.
        self.txtKitap.returnPressed.connect(self.ekle)

        # Başlangıçtaki kitap sayısını etikete yazdırıyoruz.
        self.sayiyi_yaz()

    def sayiyi_yaz(self):
        """QListWidget içindeki mevcut eleman sayısını gösterir."""
        # count() widget içindeki toplam satır/öğe sayısını döndürür.
        adet = self.listKitaplar.count()
        self.lblDurum.setText(f"Toplam kitap: {adet}")

    def ekle(self):
        """Metin kutusundaki kitabı listeye ekler."""
        # text() metni alır; strip() baştaki ve sondaki boşlukları temizler.
        kitap = self.txtKitap.text().strip()

        # Boş bir kitap adı eklenmesini önlüyoruz.
        if not kitap:
            QMessageBox.warning(self, "Eksik bilgi", "Kitap adı giriniz.")
            return

        # QListWidget'a doğrudan bir öğe ekliyoruz.
        # QListView örneğindeki gibi model.setStringList() gerekmez.
        self.listKitaplar.addItem(kitap)

        # Giriş alanını temizleyip imleci tekrar oraya taşıyoruz.
        self.txtKitap.clear()
        self.txtKitap.setFocus()

        # Kitap sayısı değiştiği için etiketi güncelliyoruz.
        self.sayiyi_yaz()

    def sil(self):
        """Kullanıcının seçtiği kitabı listeden kaldırır."""
        # currentRow() seçili öğenin sıra numarasını verir (0'dan başlar).
        # Hiçbir öğe seçili değilse -1 döndürür.
        satir = self.listKitaplar.currentRow()

        if satir == -1:
            QMessageBox.information(self, "Seçim", "Önce bir kitap seçiniz.")
            return

        # takeItem(satir) seçili satırdaki öğeyi listeden çıkarır.
        self.listKitaplar.takeItem(satir)
        self.sayiyi_yaz()

    def temizle(self):
        """Listedeki bütün kitapları kaldırır."""
        # Liste zaten boşsa işlem yapmaya gerek yok.
        if self.listKitaplar.count() == 0:
            QMessageBox.information(self, "Bilgi", "Liste zaten boş.")
            return

        # clear() listedeki tüm öğeleri siler.
        self.listKitaplar.clear()
        self.sayiyi_yaz()


if __name__ == "__main__":
    # Her PyQt masaüstü uygulamasında QApplication oluşturulur.
    app = QApplication(sys.argv)

    # Ana pencere nesnesini oluşturuyoruz.
    pencere = KitapPenceresi()
    pencere.show()

    # Qt olay döngüsünü başlatıyoruz.
    sys.exit(app.exec_())
