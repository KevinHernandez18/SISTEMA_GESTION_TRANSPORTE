from django.shortcuts import render

from rest_framework import viewsets

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

from .serializers import (
    VehiculoSerializer,
    ConductorSerializer,
    EstacionSerializer,
    RutaSerializer,
    ViajeSerializer,
    PasajeroSerializer,
    BoletoSerializer,
    MantenimientoSerializer,
    LicenciaSerializer,
    DocumentoSerializer
)

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = vehiculos.objects.all()
    serializer_class = VehiculoSerializer

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = conductores.objects.prefetch_related('licencia_set', 'documentos_set').all()
    serializer_class = ConductorSerializer

class EstacionViewSet(viewsets.ModelViewSet):
    queryset = estaciones.objects.all()
    serializer_class = EstacionSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = rutas.objects.all()
    serializer_class = RutaSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = viajes.objects.all()
    serializer_class = ViajeSerializer

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = pasajeros.objects.all()
    serializer_class = PasajeroSerializer

class BoletoViewSet(viewsets.ModelViewSet):
    queryset = boletos.objects.all()
    serializer_class = BoletoSerializer

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = mantenimientos.objects.all()
    serializer_class = MantenimientoSerializer

class LicenciaViewSet(viewsets.ModelViewSet):
    queryset = licencia.objects.select_related('id_conductor').all()
    serializer_class = LicenciaSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = documentos.objects.select_related('id_conductor').all()
    serializer_class = DocumentoSerializer
    
