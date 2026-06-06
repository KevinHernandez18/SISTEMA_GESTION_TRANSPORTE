import os
from decouple import config

# Leer el puerto .env
port = config('API_PORT')

# Ejecutar el servidor Django.

os.system(f'python manage.py runserver {port}')