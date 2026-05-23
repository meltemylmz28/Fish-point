import os
import django
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from fishing.models import FishingSpot

API_BASE = 'http://127.0.0.1:8000/api/fishing'

def list_spots():
    spots = list(FishingSpot.objects.all()[:5])
    print('Local DB spots (up to 5):')
    for s in spots:
        print(f' - {s.id}: {s.name} ({s.lat},{s.lng})')
    return spots

def call_weather(lat, lng):
    print(f'Calling weather for {lat},{lng}...')
    r = requests.get(f'{API_BASE}/weather/?lat={lat}&lng={lng}', timeout=10)
    print('Status:', r.status_code)
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print('Failed parsing response:', e)

def call_spots_by_fish(fish_name):
    print(f'Calling spots-by-fish for "{fish_name}"')
    r = requests.get(f'{API_BASE}/spots-by-fish/?fish={requests.utils.quote(fish_name)}', timeout=10)
    print('Status:', r.status_code)
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print('Failed parsing response:', e)

def call_advice(spot_id):
    print(f'Calling advice for spot {spot_id}')
    r = requests.get(f'{API_BASE}/advice/{spot_id}/', timeout=10)
    print('Status:', r.status_code)
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print('Failed parsing response:', e)

if __name__ == '__main__':
    spots = list_spots()
    if spots:
        s = spots[0]
        call_weather(s.lat, s.lng)
        call_advice(s.id)
        call_spots_by_fish('')
        call_spots_by_fish('levrek')
    else:
        print('No spots in DB to test.')
