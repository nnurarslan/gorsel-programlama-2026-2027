# Günlük Planlayıcı — PyQt5 / Qt Designer

Bu sürüm MongoDB gerektirmez. Veriler Python listesinde tutulur; uygulama kapanınca silinir.

## Çalıştırma
1. ZIP dosyasını bir klasöre çıkarın ve PyCharm ile açın.
2. Projenin terminalinde `python -m pip install -r requirements.txt` çalıştırın.
3. Tam uygulama için `main.py` dosyasını çalıştırın.
4. Yalnızca arayüzü göstermek ve derste adım adım kodlamak için `BASLANGIC.py` çalıştırın.
5. Arayüzü değiştirmek için Qt Designer ile `planlayici.ui` dosyasını açın.

.ui dosyası çalışma anında uic.loadUi ile yüklenir; pyuic5 dönüşümü gerekmez.
Qt Designer ayrı bir geliştirme aracıdır; PyQt5 kurulumu tek başına Designer uygulamasını kurmaz.

## Ders sırası
1. Designer: QCalendarWidget, QTimeEdit, QDial ve QTreeWidget özelliklerini inceleyin.
2. BASLANGIC.py: arayüzü açın. Buton işlevleri bu dosyada henüz bağlı değildir.
3. main.py: öncelik için valueChanged bağlantısını inceleyin.
4. Ekle: formu okuyun, sözlük oluşturun ve listeye ekleyin.
5. Listele: her tarih için üst öğe, her etkinlik için alt öğe oluşturun.
6. Seçim: alt öğedeki Qt.UserRole kimliğiyle kaydı bulun.
7. Güncelle ve sil işlemlerini tamamlayın.

## Davranış
- Başlangıçta liste boştur; takvimden tarih seçip etkinlik ekleyin.
- Boş veya yalnızca boşluk içeren etkinlik adı kabul edilmez.
- Aynı isimli etkinlikler ayrı kimliklerle tutulur.
- Bir etkinliği seçince bilgiler forma gelir. Tarihi değiştirip güncelleyebilirsiniz.
- Tarih başlıkları seçildiğinde Güncelle ve Sil pasiftir.
- Silme işlemi onay ister. Temizle yalnızca formu temizler.
- Kayıtlar tarih ve saate göre sıralanır. Boş tarih grupları gösterilmez.
- Takvim seçimi yeni/düzenlenen kaydın tarihidir; ağaç tüm tarihleri gösterir.

## Arayüz nesne adları
calendarWidget, lineEditEtkinlik, timeEditSaat, dialOncelik, labelOncelik,
treeWidgetEtkinlikler, pushButtonEkle, pushButtonGuncelle, pushButtonSil,
pushButtonTemizle, statusbar.
