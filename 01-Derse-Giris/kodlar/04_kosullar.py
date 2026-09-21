# if - elif - else

vize = float(input("Vize notu: "))
final = float(input("Final notu: "))

ortalama = vize * 0.40 + final * 0.60

print(f"Ortalama: {ortalama:.2f}")

if ortalama >= 60:
    print("Sonuç: Başarılı")
else:
    print("Sonuç: Başarısız")
