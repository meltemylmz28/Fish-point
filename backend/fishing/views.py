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
from .models import FishingSpot, SpotFishRelation
from .services.weather_service import get_weather

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
        av_durumu = "İdeal 🌟"
    elif temp < 10 or temp > 30:
        av_durumu = "Zor ⚠️"
    else:
        av_durumu = "Orta 📊"
    
    advice = f"""🎣 {spot.name} - {spot.district}

🌡️ Hava: {temp}°C, {weather.get('description', 'normal')}
📊 Basınç: {pressure} hPa
🎣 Av Durumu: {av_durumu}

🐟 Hedef Balıklar: {', '.join(fish_names[:5])}

✅ Öneriler:
• En iyi saat: {'Sabah 06:00-10:00' if temp > 20 else 'Öğle 11:00-15:00'}
• Önerilen yem: Mısır, Kurtçuk
• {spot.description[:100] if spot.description else 'İyi avlar!'}"""

    return Response({
        "spot_id": spot.id,
        "spot_name": spot.name,
        "district": spot.district,
        "weather": weather,
        "fish_species": fish_names,
        "advice": advice
    })