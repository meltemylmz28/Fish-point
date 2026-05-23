import os
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass')

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creating superuser '{USERNAME}'...")
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print('Superuser created.')
else:
    print(f"Superuser '{USERNAME}' already exists.")
