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
    documentos,
)


class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = estaciones
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehiculos
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    origen = EstacionSerializer(source='id_origen', read_only=True)
    destino = EstacionSerializer(source='id_destino', read_only=True)

    class Meta:
        model = rutas
        fields = '__all__'


class ConductorSerializer(serializers.ModelSerializer):
    licencias = serializers.SerializerMethodField()
    documentos = serializers.SerializerMethodField()

    class Meta:
        model = conductores
        fields = '__all__'

    def get_licencias(self, obj):
        return LicenciaSerializer(obj.licencia_set.all(), many=True).data

    def get_documentos(self, obj):
        return DocumentoSerializer(obj.documentos_set.all(), many=True).data


class ViajeSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='id_vehiculo', read_only=True)
    conductor = ConductorSerializer(source='id_conductor', read_only=True)
    ruta = RutaSerializer(source='id_ruta', read_only=True)

    class Meta:
        model = viajes
        fields = '__all__'


class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = pasajeros
        fields = '__all__'


class BoletoSerializer(serializers.ModelSerializer):
    viaje = ViajeSerializer(source='id_viaje', read_only=True)
    pasajero = PasajeroSerializer(source='id_pasajero', read_only=True)

    class Meta:
        model = boletos
        fields = '__all__'


class MantenimientoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='id_vehiculo', read_only=True)

    class Meta:
        model = mantenimientos
        fields = '__all__'


class LicenciaSerializer(serializers.ModelSerializer):
    # Allow writing the related conductor by primary key when creating/updating.
    id_conductor = serializers.PrimaryKeyRelatedField(queryset=conductores.objects.all())

    class Meta:
        model = licencia
        fields = '__all__'


class DocumentoSerializer(serializers.ModelSerializer):
    # Allow writing the related conductor by primary key when creating/updating.
    id_conductor = serializers.PrimaryKeyRelatedField(queryset=conductores.objects.all())

    class Meta:
        model = documentos
        fields = '__all__'
