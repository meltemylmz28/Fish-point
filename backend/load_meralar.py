import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from fishing.models import FishingSpot, FishSpecies, SpotFishRelation

try:
    with open('../meralar.txt', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Veri okuma basarili, yukleme basliyor...")
    spot_new = fish_new = relation_new = 0

    for ilce, meralar in data.items():
        for mera in meralar:
            coord_parts = mera['konum']['koordinat'].split(' ')
            lat = float(coord_parts[0])
            lng = float(coord_parts[2])

            spot, created = FishingSpot.objects.update_or_create(
                name=mera['mera_adi'],
                district=mera['konum']['ilce'],
                lat=lat,
                lng=lng,
                defaults={
                    'neighborhood': mera['konum']['mahalle'],
                    'spot_type': mera['konum']['tip'],
                    'water_type': mera['ekstra']['su_tipi'],
                    'min_pressure': mera['analiz']['ideal_basinc_hpa']['min'],
                    'max_pressure': mera['analiz']['ideal_basinc_hpa']['max'],
                    'min_temp': mera['analiz']['ideal_sicaklik_c']['min'],
                    'max_temp': mera['analiz']['ideal_sicaklik_c']['max'],
                    'ai_base_advice': mera['ai_tavsiye_motoru'],
                    'description': f"{mera['mera_adi']} - {mera['ekstra']['su_tipi']} mera analiz raporu.",
                },
            )
            if created:
                spot_new += 1
                print(f"Yeni mera: {mera['mera_adi']}")

            for fish_name in mera['analiz']['yaygin_turler']:
                fish, fish_created = FishSpecies.objects.get_or_create(name=fish_name)
                if fish_created:
                    fish_new += 1

                relation, rel_created = SpotFishRelation.objects.get_or_create(
                    spot=spot,
                    fish=fish,
                    defaults={'abundance': 'Yaygin'},
                )
                if rel_created:
                    relation_new += 1

    print(f"\nTamamlandi: {spot_new} yeni mera, {fish_new} yeni balik, {relation_new} yeni iliski.")

except FileNotFoundError:
    print("Hata: meralar.txt bulunamadi (proje kok dizininde olmali).")
except Exception as e:
    print(f"Hata: {e}")
