#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

# Tablas con AutoField en tu proyecto
tables = [
    ('gestion.conductores', 'id_conductor'),
    ('gestion.vehiculos', 'id_vehiculo'),
    ('gestion.estaciones', 'id_estacion'),
    ('gestion.rutas', 'id_ruta'),
    ('gestion.viajes', 'id_viaje'),
    ('gestion.pasajeros', 'id_pasajero'),
    ('gestion.boletos', 'id_boleto'),
    ('gestion.licencia', 'id_licencia'),
    ('gestion.documentos', 'id_documento'),
    ('gestion.mantenimientos', 'id_mantenimiento'),
]

print("=" * 60)
print("VERIFICANDO SECUENCIAS EN TODAS LAS TABLAS")
print("=" * 60)

for table, column in tables:
    try:
        cursor.execute(f'SELECT MAX({column}) FROM {table}')
        max_id = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT pg_get_serial_sequence('{table}', '{column}')")
        sequence_name = cursor.fetchone()[0]
        
        if sequence_name and max_id is not None:
            cursor.execute(f"SELECT last_value FROM {sequence_name}")
            last_value = cursor.fetchone()[0]
            
            status = "✓ OK" if last_value > max_id else "⚠ DESINCRONIZADA"
            print(f"{status} | {table}: MAX={max_id}, SEQUENCE={last_value}")
            
            if last_value <= max_id:
                cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH {max_id + 1}")
                print(f"   → Reseteada a {max_id + 1}")
        else:
            print(f"✓ OK | {table}: No tiene secuencia automática")
    except Exception as e:
        print(f"⚠ ERROR | {table}: {str(e)}")

connection.commit()
connection.close()
print("=" * 60)
print("Verificación completada")
