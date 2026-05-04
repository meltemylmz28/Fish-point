import os
import json
import django

# 1. Django ortamını başlat
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from fishing.models import FishingSpot

# 2. JSON verisini oku (meralar.txt dosyanın yolunu kontrol et)
try:
    with open('../meralar.txt', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Veri okuma başarılı, yükleme başlıyor...")

    for ilce, meralar in data.items():
        for mera in meralar:
            # Koordinatları "37.270 N 35.890 E" formatından ayıklıyoruz
            coord_parts = mera['konum']['koordinat'].split(' ')
            lat = float(coord_parts[0])
            lng = float(coord_parts[2])

            # Veritabanına kaydet veya varsa güncelle
            spot, created = FishingSpot.objects.update_or_create(
                name=mera['mera_adi'],
                defaults={
                    'district': mera['konum']['ilce'],
                    'neighborhood': mera['konum']['mahalle'],
                    'lat': lat,
                    'lng': lng,
                    'spot_type': mera['konum']['tip'],
                    'water_type': mera['ekstra']['su_tipi'],
                    'min_pressure': mera['analiz']['ideal_basinc_hpa']['min'],
                    'max_pressure': mera['analiz']['ideal_basinc_hpa']['max'],
                    'min_temp': mera['analiz']['ideal_sicaklik_c']['min'],
                    'max_temp': mera['analiz']['ideal_sicaklik_c']['max'],
                    'ai_base_advice': mera['ai_tavsiye_motoru'],
                    'description': f"{mera['mera_adi']} - {mera['ekstra']['su_tipi']} mera analiz raporu."
                }
            )
            if created:
                print(f"✅ Yeni yüklendi: {mera['mera_adi']}")
            else:
                print(f"🔄 Güncellendi: {mera['mera_adi']}")

    print("\n🚀 Tüm Adana meraları başarıyla veritabanına aktarıldı!")

except FileNotFoundError:
    print(
        "❌ Hata: 'meralar.txt' dosyası bulunamadı. Lütfen dosyanın backend klasörünün bir üst dizininde olduğundan emin ol.")
except Exception as e:
    print(f"❌ Bir hata oluştu: {e}")