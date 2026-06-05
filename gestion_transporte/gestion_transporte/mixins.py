import csv
import logging
import threading
from io import BytesIO
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from rest_framework import status, filters, viewsets
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPageNumberPagination

logger = logging.getLogger('gestion_transporte')

_thread_locals = threading.local()


def set_current_user(user):
    if getattr(user, 'is_authenticated', False):
        _thread_locals.user = user
    else:
        _thread_locals.user = None


def get_current_user():
    return getattr(_thread_locals, 'user', None)


class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(getattr(request, 'user', None))
        return self.get_response(request)


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(activo=False, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class AuditLog(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='audit_logs'
    )
    model_name = models.CharField(max_length=200)
    object_id = models.CharField(max_length=200)
    action = models.CharField(max_length=50)
    cambios = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'

    def __str__(self):
        return f"{self.timestamp} - {self.model_name}({self.object_id}) -> {self.action}"


class AuditableModel(models.Model):
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_%(class)s_set'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='modified_%(class)s_set'
    )
    eliminado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='deleted_%(class)s_set'
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, audit=True, **kwargs):
        user = get_current_user()
        created = self.pk is None

        if created and self.creado_por is None and user is not None:
            self.creado_por = user
        if user is not None:
            self.modificado_por = user
        super().save(*args, **kwargs)

        if audit:
            AuditLog.objects.create(
                usuario=user,
                model_name=self.__class__.__name__,
                object_id=str(self.pk),
                action='create' if created else 'update',
                cambios=None,
            )

    def delete(self, using=None, keep_parents=False):
        return self.soft_delete()

    def soft_delete(self):
        self.activo = False
        self.deleted_at = timezone.now()
        user = get_current_user()
        if user is not None:
            self.eliminado_por = user
        self.save(audit=False)
        AuditLog.objects.create(
            usuario=self.eliminado_por,
            model_name=self.__class__.__name__,
            object_id=str(self.pk),
            action='delete',
            cambios=None,
        )
        return self


class CustomResponseMixin:
    def success_response(self, data=None, message='Success', status_code=status.HTTP_200_OK, extra=None):
        payload = {
            'status': 'success',
            'code': status_code,
            'message': message,
            'data': data,
        }
        if extra:
            payload.update(extra)
        return Response(payload, status=status_code)

    def error_response(self, message='Error', status_code=status.HTTP_400_BAD_REQUEST, errors=None):
        payload = {
            'status': 'error',
            'code': status_code,
            'message': message,
        }
        if errors is not None:
            payload['errors'] = errors
        return Response(payload, status=status_code)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, list):
            return self.success_response(data=response.data, message='Lista de resultados', status_code=response.status_code)
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(data=serializer.data, message='Registro obtenido', status_code=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.success_response(data=serializer.data, message='Registro creado', status_code=status.HTTP_201_CREATED, extra={'headers': headers})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message='Registro actualizado', status_code=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        logger.info(
            'Usuario %s eliminó %s %s',
            request.user,
            instance.__class__.__name__,
            getattr(instance, 'pk', None),
        )
        return self.success_response(data=None, message='Registro eliminado (soft delete)', status_code=status.HTTP_204_NO_CONTENT)


class BaseModelViewSet(CustomResponseMixin, viewsets.ModelViewSet):
    # Use the DRF default authentication classes (configured in settings.py)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = DefaultPageNumberPagination
    ordering_fields = '__all__'
    search_fields = []
    filterset_fields = []
    required_roles = []

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(queryset, 'filter'):
            return queryset.filter(deleted_at__isnull=True)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info('Usuario %s creó %s %s', self.request.user, instance.__class__.__name__, instance.pk)

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info('Usuario %s actualizó %s %s', self.request.user, instance.__class__.__name__, instance.pk)

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        if not data:
            return self.success_response(data=[], message='No hay datos para exportar')

        # Crear workbook de Excel
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Datos'

        # Agregar encabezados
        field_names = list(data[0].keys())
        worksheet.append(field_names)

        # Agregar datos - convertir valores complejos a strings
        for item in data:
            row_data = []
            for field_name in field_names:
                value = item.get(field_name, '')
                # Convertir valores complejos a strings
                if isinstance(value, dict):
                    # Intentar extraer un campo legible del diccionario
                    if 'nombre_estacion' in value:
                        value = value.get('nombre_estacion', '')
                    elif 'nombre_ruta' in value:
                        value = value.get('nombre_ruta', '')
                    elif 'nombre' in value:
                        value = value.get('nombre', '')
                    elif 'placa' in value:
                        value = value.get('placa', '')
                    else:
                        # Si no encuentra un campo legible, usar el ID si existe
                        for key in ['id_estacion', 'id_ruta', 'id_vehiculo', 'id_conductor', 'id_pasajero', 'id']:
                            if key in value:
                                value = value.get(key, '')
                                break
                        else:
                            value = str(value)
                elif isinstance(value, list):
                    value = str(value)
                elif value is None:
                    value = ''
                row_data.append(value)
            worksheet.append(row_data)

        # Ajustar ancho de columnas automáticamente
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Guardar en buffer
        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        # Crear respuesta HTTP
        filename = f'{self.basename or self.queryset.model.__name__}.xlsx'
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Usuarios autenticados pueden leer todos los recursos.
        if request.method in SAFE_METHODS:
            return True

        required_roles = getattr(view, 'required_roles', None)
        if not required_roles:
            return True

        if request.user.is_superuser:
            return True

        user_roles = set(request.user.groups.values_list('name', flat=True))
        return bool(user_roles.intersection(required_roles))
