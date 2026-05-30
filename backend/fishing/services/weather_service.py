import requests
from django.conf import settings
from urllib.parse import quote_plus

def _wind_direction(deg):
    if deg is None:
        return "Bilinmiyor"
    directions = ['K', 'KB', 'B', 'GB', 'G', 'GD', 'D', 'KD']
    index = int(((deg + 22.5) % 360) / 45)
    return directions[index]


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
        wind = data.get("wind", {})
        sys = data.get("sys", {})
        city = data.get("name", "Bilinmiyor")
        weather_url = f"https://openweathermap.org/city/{data.get('id')}" if data.get('id') else f"https://www.google.com/search?q={quote_plus(city + ' hava durumu')}"

        return {
            "success": True,
            "temp": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": wind.get("speed", 0),
            "wind_deg": wind.get("deg"),
            "wind_direction": _wind_direction(wind.get("deg")),
            "description": data["weather"][0].get("description", ""),
            "feels_like": data["main"]["feels_like"],
            "city": city,
            "sunrise": sys.get("sunrise"),
            "sunset": sys.get("sunset"),
            "clouds": data.get("clouds", {}).get("all"),
            "weather_url": weather_url,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "temp": 20,
            "pressure": 1015,
            "humidity": 60,
            "wind_speed": 5,
            "wind_deg": None,
            "wind_direction": "Bilinmiyor",
            "description": "Hava durumu bilgisi alınamadı",
            "feels_like": 20,
            "city": "Bilinmiyor",
            "sunrise": None,
            "sunset": None,
            "clouds": None,
            "weather_url": "https://openweathermap.org",
        }