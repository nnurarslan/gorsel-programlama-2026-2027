# Fonksiyonlar

def selamla(ad):
    return f"Merhaba {ad}!"


def ortalama_hesapla(vize, final):
    return vize * 0.40 + final * 0.60


ogrenci = input("Öğrenci adı: ")
vize = float(input("Vize notu: "))
final = float(input("Final notu: "))

ortalama = ortalama_hesapla(vize, final)

print(selamla(ogrenci))
print(f"Ortalama: {ortalama:.2f}")
