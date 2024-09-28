from django.test import TestCase

# Create your tests here.
import random

# Ma'lumotlar lug'ati
malumotlar = {
    'olma': 1,
    'banan': 2,
    'nok': 3,
    'uzum': 4,
    'apelsin': 5,
    'shaftoli': 6,
    'anor': 7
}

# Tanlamoqchi bo'lgan kalit (bu kalitdan tashqari boshqa 3 ta qiymat tanlanadi)
tashqaridagi_kalit = 'banan'

# Lug'at ichidan kerakli kalitni chiqarib tashlaymiz
filtrlangan_royxat = {key: value for key, value in malumotlar.items() if key != tashqaridagi_kalit}
print(filtrlangan_royxat)

# 3 ta tasodifiy elementni tanlaymiz (qiymatlari)
tanlangan_elementlar = random.sample(list(filtrlangan_royxat.values()), 3)

print(tanlangan_elementlar)
