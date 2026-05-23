import os
import time
import django
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

API_BASE = 'http://127.0.0.1:8000/api/users'

def register(username, email, password):
    payload = {'username': username, 'email': email, 'password': password, 'password2': password}
    r = requests.post(f'{API_BASE}/register/', json=payload, timeout=10)
    print('Register status:', r.status_code)
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print('Response parse error:', e)
    return r

def login(username, password):
    payload = {'username': username, 'password': password}
    r = requests.post(f'{API_BASE}/login/', json=payload, timeout=10)
    print('Login status:', r.status_code)
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print('Response parse error:', e)
    return r

if __name__ == '__main__':
    username = f'testuser_{int(time.time())}'
    email = f'{username}@example.com'
    password = 'Testpass123!'

    # Try to register and then login with the same fresh account
    register(username, email, password)
    login(username, password)
