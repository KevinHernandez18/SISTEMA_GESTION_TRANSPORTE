import os
import sys
import django
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import requests

User = get_user_model()
USERNAME = 'Apendizkevon'
ENDPOINT = 'http://127.0.0.1:8000/gestion_transporte/api/v1/vehiculos/'

try:
    user = User.objects.get(username=USERNAME)
except User.DoesNotExist:
    print(json.dumps({'error': f"Usuario '{USERNAME}' no existe"}))
    sys.exit(1)

# Create tokens
refresh = RefreshToken.for_user(user)
access = refresh.access_token

print(json.dumps({'user_id': user.pk, 'username': user.username, 'groups': list(user.groups.values_list('name', flat=True))}))

headers = {'Authorization': f'Bearer {str(access)}'}

try:
    r = requests.get(ENDPOINT, headers=headers, timeout=10)
    print('status_code:', r.status_code)
    try:
        print('response_json:', r.json())
    except Exception:
        print('response_text:', r.text)
except Exception as e:
    print('request_error:', str(e))
