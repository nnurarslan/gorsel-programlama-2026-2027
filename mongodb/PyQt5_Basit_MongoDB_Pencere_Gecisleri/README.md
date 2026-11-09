# PyQt5 + MongoDB — Basit Pencere Geçişleri

Bu eğitim sürümünde yalnızca `pages` klasöründe dört pencere sınıfı vardır. `AppController`, `QStackedWidget`, repository ve `__init__.py` kullanılmaz. Her pencere `show()` ile açılır, önceki `close()` ile kapanır. MongoDB erişimi için yalnızca bir `database.py` bulunur.

## Kurulum
1. MongoDB Community Server'ı başlatın (localhost:27017).
2. `python -m pip install -r requirements.txt`
3. `python main.py`

## İşlemler
- Kayıt: `insert_one` ile kullanıcı ekler; e-posta benzersizdir.
- Giriş: `find_one` ile e-posta/şifre kontrol eder.
- Şifre değiştirme: `update_one` ile günceller. Bu ilk ders sürümünde `txtRecovery` adlı alan **mevcut şifre** anlamındadır; bağımsız bir kurtarma kodu mekanizması yoktur.
- Çıkış: giriş penceresine döner.

## ÖNEMLİ GÜVENLİK UYARISI
Bu sürüm **yalnızca yerel ders demonstrasyonu içindir**. Öğrencilerin CRUD mantığını rahatça görmesi için şifreler düz metin saklanmaktadır. Gerçek kullanıcı bilgileriyle, internete açık bir sunucuda veya üretim ortamında **kesinlikle kullanılmamalıdır**. Sonraki aşamada parola hash'leme, güvenli sıfırlama, oturum yönetimi ve hız sınırlama eklenmelidir.

## Önerilen ders sırası
1. `login.ui` + `login_page.py` + `main.py`: pencereyi açın.
2. Diğer `.ui` ve `pages` dosyaları: `show()` / `close()` geçişlerini kurun.
3. `database.py`: MongoDB bağlantısını ve `ping` kontrolünü anlatın.
4. `register_page.py`: `insert_one`.
5. `login_page.py`: `find_one`.
6. `reset_page.py`: `update_one`.
7. `home_page.py`: kullanıcı adını gösterin.
