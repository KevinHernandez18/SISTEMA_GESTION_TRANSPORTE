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
from rest_framework.decorators import action
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
    filterset_fields = ['id_vehiculo', 'placa', 'marca', 'modelo', 'año']
    search_fields = ['placa', 'marca', 'modelo']
    ordering_fields = ['id_vehiculo', 'placa', 'marca', 'modelo', 'año', 'fecha_creacion']


class ConductorViewSet(BaseModelViewSet):
    queryset = conductores.objects.prefetch_related('licencia_set', 'documentos_set').all()
    serializer_class = ConductorSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_conductor', 'nombre', 'celular']
    search_fields = ['nombre', 'celular']
    ordering_fields = ['id_conductor', 'nombre', 'fecha_creacion']

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        if not data:
            return self.success_response(data=[], message='No hay datos para exportar')

        serializer_field_names = list(data[0].keys())
        field_names = []
        for field_name in serializer_field_names:
            if field_name == 'licencias':
                field_names.extend(['id_licencia', 'numero_licencia'])
            elif field_name == 'documentos':
                field_names.extend(['id_documento', 'numero_documento'])
            else:
                field_names.append(field_name)

        rows = []
        for item in data:
            row = []
            for field_name in serializer_field_names:
                value = item.get(field_name, '')
                if field_name == 'licencias':
                    ids = [licencia_item.get('id_licencia') for licencia_item in value]
                    numeros = [licencia_item.get('numero_licencia') for licencia_item in value]
                    row.append(ids[0] if len(ids) == 1 else ', '.join(str(id_licencia) for id_licencia in ids))
                    row.append(numeros[0] if len(numeros) == 1 else ', '.join(str(numero) for numero in numeros))
                    continue
                elif field_name == 'documentos':
                    ids = [documento_item.get('id_documento') for documento_item in value]
                    numeros = [documento_item.get('numero_documento') for documento_item in value]
                    row.append(ids[0] if len(ids) == 1 else ', '.join(str(id_documento) for id_documento in ids))
                    row.append(numeros[0] if len(numeros) == 1 else ', '.join(str(numero) for numero in numeros))
                    continue
                elif value is None:
                    value = ''
                row.append(value)
            rows.append(row)

        return self.create_export_response(field_names, rows)


class EstacionViewSet(BaseModelViewSet):
    queryset = estaciones.objects.all()
    serializer_class = EstacionSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_estacion', 'nombre_estacion', 'ciudad', 'direccion']
    search_fields = ['nombre_estacion', 'ciudad']
    ordering_fields = ['id_estacion', 'nombre_estacion', 'ciudad', 'fecha_creacion']


class RutaViewSet(BaseModelViewSet):
    queryset = rutas.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_ruta', 'nombre_ruta', 'id_origen', 'id_destino', 'distancia_km']
    search_fields = ['nombre_ruta']
    ordering_fields = ['id_ruta', 'nombre_ruta', 'distancia_km', 'fecha_creacion']


class ViajeViewSet(BaseModelViewSet):
    queryset = viajes.objects.all()
    serializer_class = ViajeSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_viaje', 'id_vehiculo', 'id_conductor', 'id_ruta', 'fecha_salida', 'fecha_llegada']
    search_fields = ['id_vehiculo__placa', 'id_conductor__nombre', 'id_ruta__nombre_ruta']
    ordering_fields = ['id_viaje', 'fecha_salida', 'fecha_llegada', 'fecha_creacion']


class PasajeroViewSet(BaseModelViewSet):
    queryset = pasajeros.objects.all()
    serializer_class = PasajeroSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_pasajero', 'nombre', 'documento', 'celular', 'correo']
    search_fields = ['nombre', 'documento', 'correo']
    ordering_fields = ['id_pasajero', 'nombre', 'fecha_creacion']


class BoletoViewSet(BaseModelViewSet):
    queryset = boletos.objects.all()
    serializer_class = BoletoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_boleto', 'id_viaje', 'id_pasajero', 'fecha_reserva']
    search_fields = ['id_viaje__id_viaje', 'id_pasajero__nombre']
    ordering_fields = ['id_boleto', 'fecha_reserva']


class MantenimientoViewSet(BaseModelViewSet):
    queryset = mantenimientos.objects.all()
    serializer_class = MantenimientoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_mantenimiento', 'id_vehiculo', 'descripcion', 'fecha_mantenimiento', 'costo']
    search_fields = ['id_vehiculo__placa', 'descripcion']
    ordering_fields = ['id_mantenimiento', 'fecha_mantenimiento', 'costo']


class LicenciaViewSet(BaseModelViewSet):
    queryset = licencia.objects.select_related('id_conductor').all()
    serializer_class = LicenciaSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_licencia', 'id_conductor', 'numero_licencia', 'fecha_emision', 'fecha_vencimiento']
    search_fields = ['numero_licencia', 'id_conductor__nombre']
    ordering_fields = ['id_licencia', 'fecha_emision', 'fecha_vencimiento']

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        values = list(queryset.values_list('id_licencia', flat=True))
        rows = [[id_licencia] for id_licencia in values]
        return self.create_export_response(['id_licencia'], rows)


class DocumentoViewSet(BaseModelViewSet):
    queryset = documentos.objects.select_related('id_conductor').all()
    serializer_class = DocumentoSerializer
    permission_classes = [RolePermission]
    required_roles = ['Administrador', 'Supervisor']
    filterset_fields = ['id_documento', 'id_conductor', 'tipo_documento', 'numero_documento', 'fecha_nacimiento', 'fecha_emision', 'fecha_vencimiento']
    search_fields = ['tipo_documento', 'numero_documento', 'id_conductor__nombre']
    ordering_fields = ['id_documento', 'fecha_vencimiento']

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        values = list(queryset.values_list('id_documento', flat=True))
        rows = [[id_documento] for id_documento in values]
        return self.create_export_response(['id_documento'], rows)
    
