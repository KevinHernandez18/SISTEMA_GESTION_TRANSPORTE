from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    VehiculoViewSet,
    ConductorViewSet,
    EstacionViewSet,
    RutaViewSet,
    ViajeViewSet,
    PasajeroViewSet,
    BoletoViewSet,
    MantenimientoViewSet,
    LicenciaViewSet,
    DocumentoViewSet,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
        title="API de Gestión de Transporte",
        default_version='v1',
        description="Documentación Swagger para la API de Gestión de Transporte",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)   

router = DefaultRouter()

router.register(r'vehiculos', VehiculoViewSet)
router.register(r'conductores', ConductorViewSet)
router.register(r'estaciones', EstacionViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'viajes', ViajeViewSet)
router.register(r'pasajeros', PasajeroViewSet)
router.register(r'boletos', BoletoViewSet)
router.register(r'mantenimientos', MantenimientoViewSet)
router.register(r'licencias', LicenciaViewSet)
router.register(r'documentos', DocumentoViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
