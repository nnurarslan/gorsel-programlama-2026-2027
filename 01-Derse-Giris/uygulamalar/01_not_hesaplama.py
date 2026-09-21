# Mini Uygulama: Öğrenci Not Hesaplama
#
# Amaç:
# input, değişken, koşul ve fonksiyonları birlikte kullanmak.


def ortalama_hesapla(vize, final):
    return vize * 0.40 + final * 0.60


def durum_belirle(ortalama):
    if ortalama >= 60:
        return "Başarılı"
    return "Başarısız"


print("=" * 35)
print("     ÖĞRENCİ NOT HESAPLAMA")
print("=" * 35)

ad = input("Öğrenci adı: ")
vize = float(input("Vize notu: "))
final = float(input("Final notu: "))

ortalama = ortalama_hesapla(vize, final)
durum = durum_belirle(ortalama)

print("\n--- SONUÇ ---")
print(f"Öğrenci : {ad}")
print(f"Ortalama: {ortalama:.2f}")
print(f"Durum   : {durum}")
