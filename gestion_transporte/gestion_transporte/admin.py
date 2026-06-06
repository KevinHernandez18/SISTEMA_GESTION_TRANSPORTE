from django.contrib import admin
from .models import vehiculos, conductores, estaciones, rutas, viajes, pasajeros, boletos, mantenimientos, licencia, documentos

admin.site.register(vehiculos)
admin.site.register(conductores)
admin.site.register(estaciones)
admin.site.register(rutas)
admin.site.register(viajes)
admin.site.register(pasajeros)
admin.site.register(boletos)
admin.site.register(mantenimientos)
admin.site.register(licencia)
admin.site.register(documentos)