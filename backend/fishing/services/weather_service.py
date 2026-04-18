import requests
from django.conf import settings

def get_weather(lat, lng):
    """
    OpenWeatherMap API'den anlık hava durumu ve basınç bilgisi alır.
    """
    api_key = settings.OPENWEATHER_API_KEY  # Bu isim settings.py'dekiyle aynı olmalı
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric&lang=tr"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "temp": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "feels_like": data["main"]["feels_like"],
            "city": data.get("name", "Bilinmiyor")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "temp": 20,
            "pressure": 1015,
            "humidity": 60,
            "wind_speed": 5,
            "description": "Hava durumu bilgisi alınamadı",
            "city": "Bilinmiyor"
        }