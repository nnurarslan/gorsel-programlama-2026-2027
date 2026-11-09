# Basit pencere geçişleri – Görsel Programlama

## Kurulum
`python -m pip install -r requirements.txt`
`python main.py`

## Dersin kapsamı
Dört ayrı QWidget sınıfı, dört ayrı Qt Designer .ui dosyası, clicked.connect, show(), close(), QMessageBox.

**Bu aşamada MongoDB, AppController, QStackedWidget, hash ve gerçek kimlik doğrulama YOKTUR.** Girişte alanlar doluysa ana sayfa açılır; bu gerçek giriş doğrulaması değildir. Kayıt ve şifre sıfırlama butonları yalnızca form kontrolü yapar, veriyi kaydetmez.

## Kodlama sırası
1. ui/login.ui ve pages/login_page.py
2. main.py ile pencereyi açma
3. ui/register.ui ve pages/register_page.py
4. ui/reset.ui ve pages/reset_page.py
5. ui/home.ui ve pages/home_page.py
6. Her butonun show()/close() geçişini test etme

Pencere sınıfları arasındaki import'lar geçiş metotlarının içindedir; böylece karşılıklı import sorunu önlenir. `self.next_window` referansı, yeni pencerenin nesnesinin yaşamaya devam etmesini sağlar.
