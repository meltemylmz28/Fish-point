from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FishingSpot, FishSpecies, SpotFishRelation
from .serializers import FishingSpotSerializer, FishSpeciesSerializer, SpotFishRelationSerializer

class SpotListView(generics.ListAPIView):
    queryset = FishingSpot.objects.all()
    serializer_class = FishingSpotSerializer
    permission_classes = [AllowAny]

class SpotDetailView(generics.RetrieveAPIView):
    queryset = FishingSpot.objects.all()
    serializer_class = FishingSpotSerializer
    permission_classes = [AllowAny]

class FishSpeciesListView(generics.ListAPIView):
    queryset = FishSpecies.objects.all()
    serializer_class = FishSpeciesSerializer
    permission_classes = [AllowAny]

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from urllib.parse import quote_plus
from datetime import datetime
import math
from .services.weather_service import get_weather


def _hourly_fish_activity(temp, pressure, min_temp, max_temp, min_pressure, max_pressure):
    """Gün içi balık aktivitesi tahmini (0-100). Sabah/akşam zirveleri + hava uyumu."""
    temp_score = 1.0
    if temp < min_temp or temp > max_temp:
        temp_score = 0.55
    elif min_temp <= temp <= max_temp:
        temp_score = 1.0
    else:
        temp_score = 0.75

    pressure_score = 1.0
    if pressure < min_pressure or pressure > max_pressure:
        pressure_score = 0.6
    elif min_pressure <= pressure <= max_pressure:
        pressure_score = 1.0
    else:
        pressure_score = 0.8

    env_factor = (temp_score + pressure_score) / 2
    hours = []
    for hour in range(24):
        dawn = math.exp(-((hour - 6) ** 2) / 18)
        dusk = math.exp(-((hour - 18) ** 2) / 18)
        midday = 0.35 * math.exp(-((hour - 13) ** 2) / 30)
        night = 0.25 if 21 <= hour or hour <= 4 else 0.0
        raw = (dawn + dusk + midday + night) * env_factor
        activity = int(min(100, max(8, raw * 95)))
        hours.append({"hour": hour, "activity": activity})
    return hours


@api_view(['GET'])
def get_weather_for_coords(request):
    """Return weather for arbitrary coordinates (query params: lat, lng)."""
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    if lat is None or lng is None:
        return Response({'error': 'lat and lng query params required'}, status=400)
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return Response({'error': 'invalid lat or lng'}, status=400)

    weather = get_weather(lat, lng)
    return Response(weather)


@api_view(['GET'])
def spots_by_fish(request):
    """Return fishing spots that have a given fish species name (query param: fish).
    If no fish provided, returns all spots.
    """
    fish_name = request.query_params.get('fish')
    if not fish_name:
        spots = FishingSpot.objects.all()
    else:
        relations = SpotFishRelation.objects.filter(fish__name__icontains=fish_name).select_related('spot')
        spot_ids = [rel.spot.id for rel in relations]
        spots = FishingSpot.objects.filter(id__in=spot_ids)

    serializer = FishingSpotSerializer(spots, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_fishing_advice(request, spot_id):
    spot = get_object_or_404(FishingSpot, id=spot_id)
    relations = SpotFishRelation.objects.filter(spot=spot).select_related('fish')
    fish_names = [rel.fish.name for rel in relations]
    weather = get_weather(spot.lat, spot.lng)
    
    # Basit tavsiye
    temp = weather.get('temp', 20)
    pressure = weather.get('pressure', 1015)
    
    if 15 <= temp <= 25 and 1010 <= pressure <= 1020:
        av_durumu = "İdeal"
        difficulty = "Kolay"
    elif temp < 10 or temp > 30:
        av_durumu = "Zor"
        difficulty = "Zor"
    else:
        av_durumu = "Orta"
        difficulty = "Orta"

    def build_search_url(query):
        return f"https://www.google.com/search?q={quote_plus(query)}"

    fish_details = []
    for rel in relations:
        fish = rel.fish
        bait_label = fish.bait or f"{fish.name} yem"
        rod_label = fish.rod or "Orta güç olta takımı"
        line_label = fish.line or "0.20 mm misina"
        fish_details.append({
            "id": fish.id,
            "name": fish.name,
            "bait": bait_label,
            "rod": rod_label,
            "line": line_label,
            "best_season": fish.best_season or "Her mevsim",
            "purchase_bait_url": build_search_url(bait_label),
            "purchase_rod_url": build_search_url(rod_label),
            "purchase_line_url": build_search_url(line_label),
            "abundance": rel.abundance,
        })

    best_hour = 'Sabah 06:00-10:00' if temp > 20 else 'Öğle 11:00-15:00'
    bait_hint = fish_details[0]['bait'] if fish_details else 'Mısır, Kurtçuk'
    tactic_text = spot.ai_base_advice or (spot.description[:160] if spot.description else 'Sakin ve sabırlı avlanma bu noktada daha verimli.')

    advice = f"""{spot.name} - {spot.district}

Hava: {temp}°C, {weather.get('description', 'normal')}
Basınç: {pressure} hPa
Av Durumu: {av_durumu}

Hedef Balıklar: {', '.join(fish_names[:5])}

Öneriler:
• En iyi saat: {best_hour}
• Önerilen yem: {bait_hint}
• {tactic_text}"""

    daily_notes = [
        {
            "title": "Hava özeti",
            "body": f"{temp}°C • {weather.get('description', 'normal')}\nRüzgar: {weather.get('wind_speed', '-')} m/s • {weather.get('wind_direction', 'Bilinmiyor')}",
            "icon": "weather",
        },
        {
            "title": "En iyi av saati",
            "body": f"{best_hour}\nBasınç {pressure} hPa ile av durumu: {av_durumu}",
            "icon": "time",
        },
        {
            "title": "Taktik notu",
            "body": tactic_text,
            "icon": "tactic",
        },
    ]

    if fish_details:
        first_fish = fish_details[0]
        daily_notes.append({
            "title": "Ekipman",
            "body": f"{first_fish['name']}\nYem: {first_fish['bait']}\nOlta: {first_fish['rod']}\nMisina: {first_fish['line']}",
            "icon": "gear",
        })

    hourly_activity = _hourly_fish_activity(
        temp,
        pressure,
        spot.min_temp,
        spot.max_temp,
        spot.min_pressure,
        spot.max_pressure,
    )
    current_hour = datetime.now().hour

    return Response({
        "spot_id": spot.id,
        "spot_name": spot.name,
        "district": spot.district,
        "neighborhood": spot.neighborhood,
        "water_type": spot.water_type or "Tatlı su",
        "spot_type": spot.spot_type or "Bilinmeyen",
        "ai_base_advice": spot.ai_base_advice,
        "description": spot.description,
        "difficulty": difficulty,
        "av_durumu": av_durumu,
        "ideal_temp": {"min": spot.min_temp, "max": spot.max_temp},
        "ideal_pressure": {"min": spot.min_pressure, "max": spot.max_pressure},
        "hourly_activity": hourly_activity,
        "current_hour": current_hour,
        "weather": weather,
        "fish_species": fish_names,
        "fish_details": fish_details,
        "daily_notes": daily_notes,
        "advice": advice
    })