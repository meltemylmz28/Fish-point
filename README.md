# Fish-point

Fish-point, Adana çevresindeki balık meraları için Flutter frontend ve Django REST backend içeren bir yerel geliştirme projesidir.

## Proje Yapısı

- `backend/`: Django REST API, kullanıcı, sipariş ve balık noktası modelleri.
- `frontend/`: Flutter mobil uygulama, Google Maps, konum, oturum yönetimi ve spot tavsiye ekranları.
- `meralar.txt`: Proje için ilgili mera bilgilerini içerebilecek ek doküman.

## Backend Kurulumu

1. `backend` dizinine geçin:
   ```powershell
   cd "c:\Users\melte\Desktop\temiz-fish-point\backend"
   ```
2. Sanal ortam oluşturun ve etkinleştirin (önerilir).
3. Gerekli paketleri yükleyin:
   ```powershell
   py -3 -m pip install -r requirements.txt
   ```
4. Ortam dosyası varsa kopyalayın ve değerleri ayarlayın:
   ```powershell
   copy .env.example .env
   ```
5. Veritabanı migrasyonlarını çalıştırın:
   ```powershell
   py -3 manage.py migrate
   ```
6. Geliştirme sunucusunu başlatın:
   ```powershell
   py -3 manage.py runserver 0.0.0.0:8000
   ```

## Frontend Kurulumu

1. `frontend` dizinine geçin:
   ```powershell
   cd "c:\Users\melte\Desktop\temiz-fish-point\frontend"
   ```
2. Flutter bağımlılıklarını yükleyin:
   ```powershell
   flutter pub get
   ```
3. Android cihazda çalıştırmak için (fiziksel cihazda):
   ```powershell
   adb reverse tcp:8000 tcp:8000
   flutter run
   ```

> `frontend/lib/config.dart` içinde Android debug modu için backend adresi `http://localhost:8000` olarak ayarlanmıştır. Bu durumda `adb reverse` kullanmak gerekir.

## Google Maps API Anahtarı

Android için Google Maps çalışması adına `frontend/android/app/build.gradle.kts` içinde `MAPS_API_KEY` manifest placeholder olarak ayarlanır.

- `GOOGLE_MAPS_API_KEY` ortam değişkenini veya proje özelliğini kullanabilirsiniz.
- Android debug cihazlarda `manifestPlaceholders` ile anahtar sağlanmışsa Flutter tarafında ekstra bir Dart define gerekmez.

## OpenWeather API

Backend, `backend/core/settings.py` içinde `OPENWEATHER_API_KEY` ortam değişkenini kullanarak hava verilerini OpenWeatherMap üzerinden alır.

## Sosyal Giriş / Google Auth

Backend içinde Google OAuth entegrasyonu varsa şu değişkene ihtiyaç duyulur:

- `GOOGLE_OAUTH_CLIENT_ID`

Bu ayar `backend/core/settings.py` tarafından okunur.

## Çalıştırma Notları

- Backend yerel olarak `0.0.0.0:8000` üzerinde hizmet verir.
- Fiziksel Android cihaz kullandığınızda `adb reverse tcp:8000 tcp:8000` gereklidir.
- Google Maps için Android API anahtarını doğru yapılandırdığınızdan emin olun.
- Uygulama `frontend` içinden `flutter run` ile başlatılır.

## Geliştirme İpuçları

- Backend değişiklik yaptıktan sonra `py -3 manage.py migrate` çalıştırın.
- Flutter tarafında paket değişikliği sonrası `flutter pub get` yeterlidir.
- Harita görünmüyorsa API anahtarınızı ve cihazdaki ağ yönlendirmesini kontrol edin.
