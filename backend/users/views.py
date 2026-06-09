from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    GoogleLoginSerializer,
    UserSerializer,
)

User = get_user_model()  # <-- Bu çok importante!


def _build_frontend_url(request, path):
    frontend_base = getattr(settings, 'FRONTEND_URL', None)
    if frontend_base:
        base = frontend_base.rstrip('/')
    else:
        base = request.build_absolute_uri('/').rstrip('/')
    return f"{base}{path}"


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = _build_frontend_url(request, f"/verify-email?uid={uid}&token={token}")

        subject = 'Fish-Point E-posta Doğrulama'
        message = (
            f'Merhaba {user.username},\n\n'
            'Hesabınızı aktif etmek için aşağıdaki bağlantıya tıklayın:\n'
            f'{verify_url}\n\n'
            'Eğer bu işlem sizin tarafınızdan değilse, bu mesajı yok sayabilirsiniz.'
        )

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        except Exception as exc:
            print('Email verification send failed:', exc)

        response_data = {
            'user': UserSerializer(user).data,
        }
        if user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            response_data['token'] = token.key
            response_data['message'] = 'Hesabınız oluşturuldu. Giriş yapıldı.'
        else:
            response_data['message'] = 'Hesabınız oluşturuldu. Lütfen e-postanızı doğrulayın.'

        return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid', '').strip()
        token = request.data.get('token', '').strip()

        if not uid or not token:
            return Response({'detail': 'Doğrulama bilgileri eksik.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Geçersiz doğrulama bağlantısı.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Geçersiz veya süresi dolmuş doğrulama bağlantısı.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'detail': 'E-posta zaten doğrulanmış.'}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response({'detail': 'E-posta doğrulandı. Artık giriş yapabilirsiniz.'}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })


class GoogleLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
        })


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'detail': 'E-posta gerekli.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = _build_frontend_url(request, f"/reset-password?uid={uid}&token={token}")
            subject = 'Fish-Point Şifre Sıfırlama'
            message = (
                f'Merhaba {user.username},\n\n'
                'Şifre sıfırlama bağlantınız aşağıdaki gibidir:\n'
                f'{reset_url}\n\n'
                'Bu bağlantıyı kullanarak şifrenizi sıfırlayabilirsiniz.'
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
            except Exception as exc:
                print('Password reset email send failed:', exc)

        return Response({'detail': 'Eğer kayıtlı bir e-posta adresi girdiyseniz, şifre sıfırlama bağlantısı gönderildi.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid', '').strip()
        token = request.data.get('token', '').strip()
        password = request.data.get('password', '').strip()
        password2 = request.data.get('password2', '').strip()

        if not uid or not token or not password or not password2:
            return Response({'detail': 'Tüm alanları doldurun.'}, status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response({'detail': 'Şifreler eşleşmiyor.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except Exception:
            return Response({'detail': 'Geçersiz parola sıfırlama bağlantısı.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Geçersiz veya süresi dolmuş token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.is_active = True
        user.save(update_fields=['password', 'is_active'])

        return Response({'detail': 'Şifre başarıyla sıfırlandı.'})