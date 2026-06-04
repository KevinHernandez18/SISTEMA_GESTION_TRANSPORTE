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
from .mixins import BaseModelViewSet, RolePermission
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
    DocumentoSerializer,
)


class VehiculoViewSet(BaseModelViewSet):
    queryset = vehiculos.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['placa', 'marca', 'modelo', 'año', 'activo', 'fecha_creacion']
    search_fields = ['placa', 'marca', 'modelo']
    ordering_fields = ['id_vehiculo', 'placa', 'marca', 'modelo', 'año', 'fecha_creacion']


class ConductorViewSet(BaseModelViewSet):
    queryset = conductores.objects.prefetch_related('licencia_set', 'documentos_set').all()
    serializer_class = ConductorSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['nombre', 'celular', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'celular']
    ordering_fields = ['id_conductor', 'nombre', 'fecha_creacion']


class EstacionViewSet(BaseModelViewSet):
    queryset = estaciones.objects.all()
    serializer_class = EstacionSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['nombre_estacion', 'ciudad', 'activo', 'fecha_creacion']
    search_fields = ['nombre_estacion', 'ciudad']
    ordering_fields = ['id_estacion', 'nombre_estacion', 'ciudad', 'fecha_creacion']


class RutaViewSet(BaseModelViewSet):
    queryset = rutas.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['nombre_ruta', 'id_origen', 'id_destino', 'activo', 'fecha_creacion']
    search_fields = ['nombre_ruta']
    ordering_fields = ['id_ruta', 'nombre_ruta', 'distancia_km', 'fecha_creacion']


class ViajeViewSet(BaseModelViewSet):
    queryset = viajes.objects.all()
    serializer_class = ViajeSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_vehiculo', 'id_conductor', 'id_ruta', 'fecha_salida', 'fecha_llegada', 'activo']
    search_fields = ['id_vehiculo__placa', 'id_conductor__nombre', 'id_ruta__nombre_ruta']
    ordering_fields = ['id_viaje', 'fecha_salida', 'fecha_llegada', 'fecha_creacion']


class PasajeroViewSet(BaseModelViewSet):
    queryset = pasajeros.objects.all()
    serializer_class = PasajeroSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['nombre', 'documento', 'correo', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'documento', 'correo']
    ordering_fields = ['id_pasajero', 'nombre', 'fecha_creacion']


class BoletoViewSet(BaseModelViewSet):
    queryset = boletos.objects.all()
    serializer_class = BoletoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_viaje', 'id_pasajero', 'fecha_reserva', 'activo']
    search_fields = ['id_viaje__id_viaje', 'id_pasajero__nombre']
    ordering_fields = ['id_boleto', 'fecha_reserva']


class MantenimientoViewSet(BaseModelViewSet):
    queryset = mantenimientos.objects.all()
    serializer_class = MantenimientoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_vehiculo', 'fecha_mantenimiento', 'costo', 'activo']
    search_fields = ['id_vehiculo__placa', 'descripcion']
    ordering_fields = ['id_mantenimiento', 'fecha_mantenimiento', 'costo']


class LicenciaViewSet(BaseModelViewSet):
    queryset = licencia.objects.select_related('id_conductor').all()
    serializer_class = LicenciaSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_conductor', 'numero_licencia', 'fecha_emision', 'fecha_vencimiento', 'activo']
    search_fields = ['numero_licencia', 'id_conductor__nombre']
    ordering_fields = ['id_licencia', 'fecha_emision', 'fecha_vencimiento']


class DocumentoViewSet(BaseModelViewSet):
    queryset = documentos.objects.select_related('id_conductor').all()
    serializer_class = DocumentoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_conductor', 'tipo_documento', 'numero_documento', 'fecha_vencimiento', 'activo']
    search_fields = ['tipo_documento', 'numero_documento', 'id_conductor__nombre']
    ordering_fields = ['id_documento', 'fecha_vencimiento']
    
