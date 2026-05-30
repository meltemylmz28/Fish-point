import re

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

User = get_user_model()  # <-- Bu önemli!


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_username(self, value):
        username = value.strip().lower()
        username = username.replace('ı', '')
        username = re.sub(r'[^a-z0-9._-]', '', username)

        if not username:
            raise serializers.ValidationError('Geçerli bir kullanıcı adı girin.')
        if len(username) < 4:
            raise serializers.ValidationError('Kullanıcı adı en az 4 karakter olmalı.')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError('Bu kullanıcı adı zaten alınmış.')
        return username

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('Bu e-posta zaten kayıtlı.')
        return email

    def validate_password(self, value):
        password = value.strip()
        if len(password) < 8:
            raise serializers.ValidationError('Şifre en az 8 karakter olmalı.')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('Şifre en az bir büyük harf içermeli.')
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError('Şifre en az bir küçük harf içermeli.')
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError('Şifre en az bir rakam içermeli.')
        if not re.search(r'[!@#\$%\^&\*()_+\-=\[\]{};:\'"\\|,.<>\/?`~]', password):
            raise serializers.ValidationError('Şifre en az bir özel karakter içermeli.')
        if ' ' in password:
            raise serializers.ValidationError('Şifre boşluk içeremez.')
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifreler eşleşmiyor."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save(update_fields=['is_active'])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            user_obj = User.objects.filter(email__iexact=username).first()
            if user_obj:
                user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise serializers.ValidationError("Kullanıcı adı veya şifre hatalı.")

        attrs['user'] = user
        return attrs


def _make_unique_username(base_username):
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

    def validate_id_token(self, value):
        try:
            google_request = google_requests.Request()
            idinfo = id_token.verify_oauth2_token(value, google_request)
        except Exception:
            raise serializers.ValidationError("Geçersiz Google kimlik doğrulama jetonu.")

        if not idinfo.get('email') or not idinfo.get('email_verified'):
            raise serializers.ValidationError("Google hesabı doğrulanamadı.")

        client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', None)
        if client_id and idinfo.get('aud') != client_id:
            raise serializers.ValidationError("Google client ID uyuşmuyor.")

        return idinfo

    def validate(self, attrs):
        idinfo = attrs['id_token']
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            username_base = email.split('@')[0].lower()
            username = _make_unique_username(username_base)
            user = User.objects.create_user(username=username, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        attrs['user'] = user
        return attrs


