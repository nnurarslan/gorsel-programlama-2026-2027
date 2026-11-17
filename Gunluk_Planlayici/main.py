"""Qt Designer arayüzüyle, bellekte çalışan günlük planlayıcı."""
import sys
from pathlib import Path
from uuid import uuid4
from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime, Qt, QLocale
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QMessageBox


class Planlayici(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).with_name('planlayici.ui')), self)
        self.kayitlar = []  # Uygulama kapanınca silinir.
        self.secili_id = None
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.timeEditSaat.setTime(QTime.currentTime())
        self.dialOncelik.valueChanged.connect(self.oncelik_goster)
        self.pushButtonEkle.clicked.connect(self.ekle)
        self.pushButtonGuncelle.clicked.connect(self.guncelle)
        self.pushButtonSil.clicked.connect(self.sil)
        self.pushButtonTemizle.clicked.connect(self.temizle)
        self.treeWidgetEtkinlikler.itemSelectionChanged.connect(self.secim_degisti)
        self.oncelik_goster(self.dialOncelik.value())
        self.secim_degisti()

    def oncelik_goster(self, deger):
        self.labelOncelik.setText(f'Öncelik: {deger} / 5')

    def form_verisi(self):
        baslik = self.lineEditEtkinlik.text().strip()
        if not baslik:
            QMessageBox.warning(self, 'Eksik bilgi', 'Etkinlik adını giriniz.')
            self.lineEditEtkinlik.setFocus()
            return None
        return dict(baslik=baslik,
                    tarih=self.calendarWidget.selectedDate().toString('yyyy-MM-dd'),
                    saat=self.timeEditSaat.time().toString('HH:mm'),
                    oncelik=self.dialOncelik.value())

    def ekle(self):
        veri = self.form_verisi()
        if veri is None:
            return
        veri['id'] = str(uuid4())
        self.kayitlar.append(veri)
        self.listele()
        self.temizle()

    def listele(self):
        agac = self.treeWidgetEtkinlikler
        agac.blockSignals(True)
        agac.clear()
        gruplar = {}
        tr = QLocale(QLocale.Turkish, QLocale.Turkey)
        for kayit in sorted(self.kayitlar, key=lambda k: (k['tarih'], k['saat'], k['baslik'])):
            tarih = kayit['tarih']
            if tarih not in gruplar:
                etiket = tr.toString(QDate.fromString(tarih, 'yyyy-MM-dd'), 'd MMMM yyyy')
                ust = QTreeWidgetItem(agac, [etiket, '', ''])
                font = ust.font(0)
                font.setBold(True)
                ust.setFont(0, font)
                gruplar[tarih] = ust
            alt = QTreeWidgetItem(gruplar[tarih], [kayit['baslik'], kayit['saat'], str(kayit['oncelik'])])
            alt.setData(0, Qt.UserRole, kayit['id'])
        agac.expandAll()
        agac.setColumnWidth(0, 330)
        agac.setColumnWidth(1, 90)
        agac.blockSignals(False)
        self.secim_degisti()
        self.statusbar.showMessage(f'{len(self.kayitlar)} etkinlik • Kayıtlar yalnızca bellekte tutulur.')

    def secim_degisti(self):
        item = self.treeWidgetEtkinlikler.currentItem()
        self.secili_id = item.data(0, Qt.UserRole) if item else None
        self.pushButtonGuncelle.setEnabled(self.secili_id is not None)
        self.pushButtonSil.setEnabled(self.secili_id is not None)
        if self.secili_id is None:
            return
        kayit = next(k for k in self.kayitlar if k['id'] == self.secili_id)
        self.lineEditEtkinlik.setText(kayit['baslik'])
        self.calendarWidget.setSelectedDate(QDate.fromString(kayit['tarih'], 'yyyy-MM-dd'))
        self.timeEditSaat.setTime(QTime.fromString(kayit['saat'], 'HH:mm'))
        self.dialOncelik.setValue(kayit['oncelik'])

    def guncelle(self):
        if self.secili_id is None:
            return
        veri = self.form_verisi()
        if veri is None:
            return
        kayit = next(k for k in self.kayitlar if k['id'] == self.secili_id)
        kayit.update(veri)
        self.listele()
        self.temizle()

    def sil(self):
        if self.secili_id is None:
            return
        cevap = QMessageBox.question(self, 'Etkinliği sil', 'Seçili etkinlik silinsin mi?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.kayitlar = [k for k in self.kayitlar if k['id'] != self.secili_id]
            self.listele()
            self.temizle()

    def temizle(self):
        self.treeWidgetEtkinlikler.clearSelection()
        self.treeWidgetEtkinlikler.setCurrentItem(None)
        self.secili_id = None
        self.lineEditEtkinlik.clear()
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.timeEditSaat.setTime(QTime(9, 0))
        self.dialOncelik.setValue(3)
        self.pushButtonGuncelle.setEnabled(False)
        self.pushButtonSil.setEnabled(False)
        self.lineEditEtkinlik.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    pencere = Planlayici()
    pencere.show()
    sys.exit(app.exec_())
