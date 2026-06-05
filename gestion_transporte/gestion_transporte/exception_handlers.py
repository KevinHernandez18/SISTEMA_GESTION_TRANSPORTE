from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
)


def custom_exception_handler(exc, context):
    """
    Custom exception handler que devuelve respuestas JSON consistentes
    para errores de autenticación y autorización.
    """
    response = exception_handler(exc, context)

    if response is None:
        return None

    # Manejo específico de excepciones de autenticación
    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Las credenciales de autenticación no han sido provistas.',
                'detail': 'Debes incluir un token válido en el header Authorization: Bearer <token>',
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, AuthenticationFailed):
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Fallo en la autenticación.',
                'detail': str(exc.detail) if hasattr(exc, 'detail') else 'El token es inválido, expirado o ha sido revocado.',
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_403_FORBIDDEN,
                'message': 'Permiso denegado.',
                'detail': str(exc.detail) if hasattr(exc, 'detail') else 'No tienes permisos para acceder a este recurso. Verifica tu rol y permisos.',
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Personalizar otras excepciones
    if status.is_client_error(response.status_code):
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                'status': 'error',
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Token inactivo o no válido.',
                'detail': response.data.get('detail', 'El token no se encuentra activo o ha expirado.'),
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'status': 'error',
                'code': status.HTTP_403_FORBIDDEN,
                'message': 'Acceso denegado.',
                'detail': response.data.get('detail', 'No tienes permisos suficientes para realizar esta acción.'),
            }
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Solicitud inválida.',
                'errors': response.data,
            }
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Recurso no encontrado.',
                'detail': response.data.get('detail', 'El recurso solicitado no existe.'),
            }

    return response
