# Fish-point

## Kurulum & Çalıştırma

### Backend

1. `backend` klasörüne girin:
   ```powershell
   cd "c:\Users\melte\Desktop\temiz-fish-point\backend"
   ```
2. `.env.example` dosyasını kopyalayın ve gerçek değerlerle doldurun:
   ```powershell
   copy .env.example .env
   ```
3. Paketleri yükleyin:
   ```powershell
   py -3 -m pip install -r requirements.txt
   ```
4. Veritabanını hazır hale getirin:
   ```powershell
   py -3 manage.py migrate
   ```
5. Geliştirme sunucusunu başlatın:
   ```powershell
   py -3 manage.py runserver 0.0.0.0:8000
   ```

### Frontend

1. `frontend` klasörüne girin:
   ```bash
   cd "c:\Users\melte\Desktop\temiz-fish-point\frontend"
   ```
2. Paketleri güncelleyin:
   ```bash
   flutter pub get
   ```
3. Uygulamayı çalıştırın:
   ```bash
   flutter run
   ```

## Sosyal Giriş (Google)

### Backend Ayarları

Aşağıdaki ortam değişkenini ayarlamanız gerekiyor:

- `GOOGLE_OAUTH_CLIENT_ID`

Bu değer `backend/core/settings.py` içinde okunuyor.

### Google

- Google Cloud Console'dan Android için OAuth Client ID oluşturun.
- Android için paket adı ve SHA-1 sertifika parmak izini kullanın.
- iOS için gerekli yapılandırma varsa, ilgili `Info.plist` ayarlarını ekleyin.

## Notlar

- Local geliştirme için backend `0.0.0.0:8000` üzerinde çalışıyor.
- Test admin kullanıcı: `admin` / `adminpass` (güvenli değildir, değiştirin).
