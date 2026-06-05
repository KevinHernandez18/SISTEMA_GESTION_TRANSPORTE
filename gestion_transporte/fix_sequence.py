#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

# Obtener el máximo ID actual en la tabla conductores
cursor.execute('SELECT MAX(id_conductor) FROM gestion.conductores')
max_id = cursor.fetchone()[0]
print(f"✓ ID máximo en tabla conductores: {max_id}")

# Obtener la secuencia actual
cursor.execute("SELECT pg_get_serial_sequence('gestion.conductores', 'id_conductor')")
sequence_name = cursor.fetchone()[0]
print(f"✓ Secuencia: {sequence_name}")

if sequence_name and max_id is not None:
    # Establecer la secuencia al siguiente valor después del máximo ID
    next_id = max_id + 1
    cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH {next_id}")
    print(f"✓ Secuencia reseteada a: {next_id}")
    connection.commit()
    print("✓ Cambio guardado exitosamente")
else:
    print("⚠ No se pudo determinar la secuencia o la tabla está vacía")

connection.close()
