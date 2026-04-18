# fishing/services/llm_service.py
from django.conf import settings
from google import genai
from google.genai import types
def get_llm_advice(spot_name, district, fish_species, current_weather, spot_type):

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""Sen bir balıkçılık uzmanısın. Kullanıcıya aşağıdaki bilgilere göre av tavsiyesi ver.

Mera: {spot_name}
İlçe: {district}
Su Tipi: {spot_type}

Bu bölgede bulunan balıklar: {', '.join(fish_species)}

Şu anki hava durumu:
- Sıcaklık: {current_weather.get('temp', '?')}°C
- Basınç: {current_weather.get('pressure', '?')} hPa
- Nem: {current_weather.get('humidity', '?')}%
- Rüzgar: {current_weather.get('wind_speed', '?')} m/s
- Gökyüzü: {current_weather.get('description', '?')}

Lütfen TÜRKÇE olarak şu başlıklarda KISA (max 200 kelime) bir tavsiye yaz:

1. 🎯 Bugün avlanmaya uygun mu? (Kısa değerlendirme)
2. 🐟 Hangi balık türü daha aktif olur?
3. 🎣 Hangi yem ve ekipman kullanılmalı?
4. ⏰ Günün hangi saatleri tercih edilmeli?

Tavsiyeni maddeler halinde ve samimi bir dille yaz."""

    try:
        # 1. Deneme: En güncel ve hızlı ana model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return {
            "success": True,
            "advice": response.text,
            "model": "gemini-2.0-flash"
        }

    except Exception as e:
        print(f"Ana model (2.0) hatası: {str(e)}")  # Hata takibi için

        try:
            # 2. Deneme: Yedek plan (Fallback) - Stabil 1.5 modeli
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return {
                "success": True,
                "advice": response.text,
                "model": "gemini-1.5-flash"
            }
        except Exception as e2:
            print(f"Yedek model (1.5) hatası: {str(e2)}")

            # 3. Deneme: Eğer API tamamen başarısız olursa (Kota/İnternet vb.) Manuel Tavsiye
            return {
                "success": False,
                "error": str(e2),
                "advice": f"""
🎣 {spot_name} için hızlı av rehberi:

📍 Konum: {district} - {spot_type}
🐟 Hedefler: {', '.join(fish_species[:3])}
🌡️ Hava: {current_weather.get('temp', '?')}°C, {current_weather.get('description', 'açık')}

✅ Öneriler:
• Hava durumu {'balıkçılık için elverişli' if 15 <= current_weather.get('temp', 20) <= 28 else 'biraz zorlayıcı'} görünüyor.
• Bugün {fish_species[0] if fish_species else 'yerel balıklar'} için şansınızı deneyebilirsiniz.
• Doğal yemler ve ince takım kullanmanızı öneririz.
• Sabah suyun ilk ışıkları veya gün batımı en verimli saatlerdir.

Not: Yapay zeka servisine şu an ulaşılamıyor, bu bilgiler otomatik üretilmiştir.
"""
            }