from rest_framework import serializers

from .models import (
    vehiculos,
    conductores,
    estaciones,
    rutas,
    viajes,
    pasajeros,
    boletos,
    mantenimientos,
    licencia,
    documentos
)

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehiculos
        fields = '__all__'

class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = estaciones
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = rutas
        fields = '__all__'

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = viajes
        fields = '__all__'

class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = pasajeros
        fields = '__all__'

class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = boletos
        fields = '__all__'

class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = mantenimientos
        fields = '__all__'

class LicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = licencia
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = documentos
        fields = '__all__'

class ConductorSerializer(serializers.ModelSerializer):
    licencia = LicenciaSerializer(source='licencia_set', many=True, read_only=True)
    documento = DocumentoSerializer(source='documentos_set', many=True, read_only=True)

    class Meta:
        model = conductores
        fields = '__all__'
