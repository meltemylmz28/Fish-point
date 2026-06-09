import json
from django.core.management.base import BaseCommand
from fishing.models import FishingSpot, FishSpecies, SpotFishRelation

class Command(BaseCommand):
    help = 'meralar.txt JSON dosyasından tüm verileri yükler'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='JSON dosyasının yolu')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        spot_count = 0
        fish_count = 0
        relation_count = 0
        
        for ilce, spots in data.items():
            self.stdout.write(f"\n📌 {ilce.upper()} ilçesi işleniyor...")
            
            for spot_data in spots:
                # Koordinatları parse et
                coords = spot_data['konum']['koordinat'].split()
                lat = float(coords[0])
                lng = float(coords[2])
                
                # Mera oluştur
                spot, created = FishingSpot.objects.get_or_create(
                    name=spot_data['mera_adi'],
                    district=spot_data['konum']['ilce'],
                    lat=lat,
                    lng=lng,
                    defaults={
                        'description': f"Tip: {spot_data['konum']['tip']}\nSu: {spot_data['ekstra']['su_tipi']}\n{spot_data.get('ai_tavsiye_motoru', '')}",
                        'spot_type': spot_data['konum']['tip'],
                        'water_type': spot_data['ekstra'].get('su_tipi', ''),
                        'ai_base_advice': spot_data.get('ai_tavsiye_motoru', ''),
                    }
                )
                
                if created:
                    spot_count += 1
                    self.stdout.write(f"  ✅ {spot.name}")
                
                # Balık türleri
                for fish_name in spot_data['analiz']['yaygin_turler']:
                    fish, _ = FishSpecies.objects.get_or_create(name=fish_name)
                    if _:
                        fish_count += 1
                    
                    relation, _ = SpotFishRelation.objects.get_or_create(
                        spot=spot, fish=fish,
                        defaults={'abundance': 'Yaygın'}
                    )
                    if _:
                        relation_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ {spot_count} mera, {fish_count} balık, {relation_count} ilişki eklendi."))