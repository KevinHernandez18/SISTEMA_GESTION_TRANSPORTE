# Sistema de Gestion de Transporte

Este proyecto corresponde a un API REST diseñado para la administracion integral de un sistema de transporte. Permite gestionar vehiculos, conductores, estaciones, rutas, viajes, pasajeros, boletos, mantenimientos, licencias y documentos desde una arquitectura basada en Django REST Framework.

El proyecto incorpora funcionalidades propias de una API empresarial: autenticacion JWT, permisos por rol, documentacion Swagger, versionado, respuestas JSON estandarizadas, paginacion, filtros, busqueda, ordenamiento dinamico, auditoria automatica, soft delete, logging de operaciones y exportacion de datos a Excel.

## Resumen Ejecutivo

`SISTEMA_GESTION_TRANSPORTE` centraliza la operacion de una plataforma de transporte. Su objetivo es organizar y exponer de forma segura la informacion operativa del negocio: recursos fisicos, conductores, documentos legales, rutas, viajes, pasajeros, reservas y mantenimientos.

La API no se limita a operaciones CRUD basicas. Esta disenada para soportar consumo real desde clientes externos, paneles administrativos, integraciones y herramientas de reporte.

## Stack Tecnologico

| Tecnologia | Uso dentro del proyecto |
|---|---|
| Python | Lenguaje principal del backend. |
| Django 6.x | Framework base del proyecto. |
| Django REST Framework | Construccion de endpoints REST, ViewSets y serializers. |
| PostgreSQL | Base de datos relacional principal. |
| SimpleJWT | Autenticacion mediante tokens JWT. |
| django-filter | Filtros avanzados sobre endpoints. |
| drf-yasg | Documentacion Swagger y Redoc. |
| openpyxl | Generacion de archivos Excel para exportaciones. |

## Ruta Base Del API

La API se expone bajo la ruta:

```http
/gestion_transporte/api/v1/
```

Documentacion interactiva:

```http
/gestion_transporte/swagger/
/gestion_transporte/redoc/
```

Autenticacion:

```http
POST /gestion_transporte/api/v1/auth/token/
POST /gestion_transporte/api/v1/auth/token/refresh/
```

## Modulos Funcionales

| Modulo | Endpoint | Funcion principal |
|---|---|---|
| Vehiculos | `/vehiculos/` | Administra placa, marca, modelo y ano del vehiculo. |
| Conductores | `/conductores/` | Gestiona conductores e incluye licencias y documentos relacionados. |
| Estaciones | `/estaciones/` | Registra estaciones por nombre, ciudad y direccion. |
| Rutas | `/rutas/` | Define recorridos entre estacion de origen y estacion de destino. |
| Viajes | `/viajes/` | Relaciona vehiculo, conductor y ruta con fechas de salida y llegada. |
| Pasajeros | `/pasajeros/` | Administra datos de pasajeros, documento, celular y correo. |
| Boletos | `/boletos/` | Registra reservas asociando pasajeros con viajes. |
| Mantenimientos | `/mantenimientos/` | Gestiona mantenimientos de vehiculos, descripcion, fecha y costo. |
| Licencias | `/licencias/` | Administra licencias asociadas a conductores. |
| Documentos | `/documentos/` | Administra documentos personales asociados a conductores. |

## Funcionalidades

| # | Ajuste | Objetivo | Ejemplo en esta API |
|---|---|---|---|
| 1 | Documentacion Swagger | Generar documentacion automatica y probar endpoints desde navegador. | `/gestion_transporte/swagger/` |
| 2 | Versionado de API | Organizar cambios futuros sin romper clientes existentes. | `/gestion_transporte/api/v1/conductores/` |
| 3 | Respuestas JSON personalizadas | Estandarizar la estructura de exito y error. | `{ "status": "success", "code": 200, "message": "...", "data": ... }` |
| 4 | Paginacion | Controlar grandes cantidades de registros. | `?page=1&page_size=10` |
| 5 | Filtros de busqueda | Permitir consultas mas precisas. | `/conductores/?nombre=Juan` |
| 6 | Ordenamiento dinamico | Ordenar resultados por campos permitidos. | `?ordering=nombre` |
| 7 | Soft delete | Evitar eliminacion fisica de registros. | Marca `deleted_at` y `activo=false`. |
| 8 | Auditoria automatica | Registrar quien crea, modifica o elimina registros. | `creado_por`, `modificado_por`, `eliminado_por`. |
| 9 | Autenticacion JWT | Proteger endpoints mediante token seguro. | `Authorization: Bearer <token>` |
| 10 | Permisos por rol | Controlar acciones segun el grupo del usuario. | Escritura solo para `Administrador` o `Supervisor`. |
| 11 | Relaciones anidadas | Mostrar informacion completa de objetos relacionados. | Conductores incluyen `licencias` y `documentos`. |
| 12 | Exportacion de datos | Generar reportes operativos en Excel. | `/conductores/export/`, `/licencias/export/`, `/documentos/export/`. |
| 13 | Logging de operaciones | Registrar actividad relevante del API. | Archivo `api_operations.log`. |
| 14 | Manejo personalizado de errores | Devolver mensajes claros y consistentes. | Errores `401`, `403`, `400` y `404` personalizados. |

## Seguridad

La API utiliza autenticacion JWT. Para obtener un token se consume:

```http
POST /gestion_transporte/api/v1/auth/token/
```

El cual al realizar log in entrega 1 token de acceso <ACCESS_TOKEN> y un token para refresh <REFRESH_TOKEN>.

```http
{
    "refresh" : "<REFRESH_TOKEN>",
    "access" : "<ACCESS_TOKEN>"
}
```

El refresh token cumple la función de generar un nuevo token una vez el token access deje de ser aceptado por el API. Para acceder al refresh token se consume:

```http
POST /gestion_transporte/api/v1/auth/token/refresh/
```

El cual devuelve un access token nuevo:

```http
{
    "access" : "<ACCESS_TOKEN>"
}
```

Luego, las solicitudes protegidas deben incluir el encabezado:

```http
Authorization: Bearer <ACCESS_TOKEN>
```


El sistema tambien implementa permisos por rol. Los usuarios autenticados pueden consultar recursos, mientras que las operaciones de escritura, actualizacion o eliminacion se restringen a roles autorizados como `Administrador` o `Supervisor`.

## Respuestas JSON Estandarizadas

Las respuestas exitosas siguen una estructura consistente:

```json
{
  "status": "success",
  "code": 200,
  "message": "Lista de resultados",
  "data": []
}
```

Las respuestas de error tambien se normalizan:

```json
{
  "status": "error",
  "code": 401,
  "message": "Fallo en la autenticacion.",
  "detail": "El token es invalido, expirado o ha sido revocado."
}
```

Esto facilita el consumo desde frontends, clientes moviles, integraciones externas o herramientas como Postman.

## Paginacion

La paginacion esta configurada por defecto en 10 registros por pagina y permite controlar el tamano de respuesta:

```http
GET /gestion_transporte/api/v1/conductores/?page=1&page_size=5
```

Respuesta paginada:

```json
{
  "status": "success",
  "code": 200,
  "message": "Lista de resultados",
  "data": [],
  "pagination": {
    "current_page": 1,
    "page_size": 5,
    "total_pages": 10,
    "total_items": 50
  }
}
```

Tambien se puede solicitar una respuesta sin paginacion usando:

```http
?page_size=-1
```

## Filtros, Busqueda Y Ordenamiento

Cada ViewSet define campos habilitados para filtros, busqueda y ordenamiento. Esto permite realizar consultas mas utiles sin crear endpoints adicionales.

Ejemplos:

```http
GET /gestion_transporte/api/v1/vehiculos/?search=ABC
GET /gestion_transporte/api/v1/conductores/?ordering=nombre
GET /gestion_transporte/api/v1/licencias/?numero_licencia=LIC-10001
GET /gestion_transporte/api/v1/viajes/?ordering=fecha_salida
```

## Relaciones Entre Entidades

La API modela relaciones importantes del negocio:

| Relacion | Descripcion |
|---|---|
| Conductor - Licencia | Un conductor puede tener licencias asociadas. |
| Conductor - Documento | Un conductor puede tener documentos asociados. |
| Ruta - Estaciones | Una ruta tiene estacion de origen y estacion de destino. |
| Viaje - Vehiculo | Un viaje se realiza con un vehiculo especifico. |
| Viaje - Conductor | Un viaje se asigna a un conductor. |
| Viaje - Ruta | Un viaje sigue una ruta determinada. |
| Boleto - Pasajero | Un boleto pertenece a un pasajero. |
| Boleto - Viaje | Un boleto reserva cupo en un viaje. |
| Mantenimiento - Vehiculo | Un mantenimiento se registra sobre un vehiculo. |

Los serializers tambien muestran informacion relacionada. Por ejemplo, el serializer de conductores incluye `licencias` y `documentos` embebidos, y el serializer de viajes incluye datos del vehiculo, conductor y ruta.

## Auditoria Automatica

Los modelos principales heredan de `AuditableModel`, lo que agrega trazabilidad sobre los registros:

| Campo | Funcion |
|---|---|
| `creado_por` | Usuario que creo el registro. |
| `modificado_por` | Usuario que modifico el registro por ultima vez. |
| `eliminado_por` | Usuario que elimino logicamente el registro. |
| `fecha_creacion` | Fecha de creacion. |
| `fecha_modificacion` | Fecha de ultima modificacion. |
| `deleted_at` | Fecha de eliminacion logica. |
| `activo` | Estado operativo del registro. |

El middleware `ThreadLocalMiddleware` captura el usuario autenticado de la solicitud y permite asignarlo automaticamente durante operaciones de creacion, actualizacion o eliminacion.

## Soft Delete

Cuando se elimina un registro desde la API, no se borra fisicamente de la base de datos. En su lugar:

- Se marca `activo=false`.
- Se asigna una fecha en `deleted_at`.
- Se registra el usuario en `eliminado_por`.
- Se genera una entrada de auditoria.

Esto protege la informacion historica y permite mantener trazabilidad de las operaciones.

## Exportacion A Excel

La API genera reportes en formato `.xlsx` usando `openpyxl`.

Endpoints de exportacion:

```http
GET /gestion_transporte/api/v1/conductores/export/
GET /gestion_transporte/api/v1/licencias/export/
GET /gestion_transporte/api/v1/documentos/export/
```

El export de conductores esta personalizado para incluir informacion clave de relaciones:

| Campo exportado | Descripcion |
|---|---|
| `id_licencia` | Identificador de la licencia relacionada. |
| `numero_licencia` | Numero de licencia del conductor. |
| `id_documento` | Identificador del documento relacionado. |
| `numero_documento` | Numero del documento del conductor. |

Ejemplo:

```http
GET /gestion_transporte/api/v1/conductores/export/
Authorization: Bearer <ACCESS_TOKEN>
```

## Logging De Operaciones

El sistema registra operaciones relevantes del API mediante el logger `gestion_transporte`. Las acciones de creacion, actualizacion y eliminacion se registran en consola y en archivo:

```text
gestion_transporte/api_operations.log
```

Esto permite monitorear actividad y revisar eventos importantes durante la operacion del sistema.

## Manejo De Errores

El proyecto cuenta con un manejador personalizado de excepciones. Su objetivo es devolver respuestas mas claras para errores frecuentes:

| Codigo | Caso |
|---|---|
| `400` | Solicitud invalida. |
| `401` | Token ausente, invalido o expirado. |
| `403` | Usuario sin permisos suficientes. |
| `404` | Recurso no encontrado. |

Ejemplo de error de permisos:

```json
{
  "status": "error",
  "code": 403,
  "message": "Permiso denegado.",
  "detail": "No tienes permisos para acceder a este recurso. Verifica tu rol y permisos."
}
```

## Estructura Del Proyecto

| Ruta | Funcion |
|---|---|
| `gestion_transporte/backend/settings.py` | Configuracion global: apps, base de datos, JWT, Swagger, logging y DRF. |
| `gestion_transporte/backend/urls.py` | Entrada principal de rutas del proyecto. |
| `gestion_transporte/backend/asgi.py` | Configuracion ASGI. |
| `gestion_transporte/backend/wsgi.py` | Configuracion WSGI. |
| `gestion_transporte/gestion_transporte/models.py` | Entidades y relaciones de base de datos. |
| `gestion_transporte/gestion_transporte/serializers.py` | Conversion de modelos a JSON y manejo de relaciones anidadas. |
| `gestion_transporte/gestion_transporte/views.py` | ViewSets, permisos, filtros, busqueda, ordenamiento y exportaciones. |
| `gestion_transporte/gestion_transporte/urls.py` | Registro de endpoints mediante `DefaultRouter`. |
| `gestion_transporte/gestion_transporte/mixins.py` | Respuestas personalizadas, auditoria, soft delete, exportacion y permisos. |
| `gestion_transporte/gestion_transporte/pagination.py` | Paginacion personalizada con metadata. |
| `gestion_transporte/gestion_transporte/exception_handlers.py` | Respuestas estandarizadas para errores. |
| `gestion_transporte/gestion_transporte/admin.py` | Registro de modelos en Django Admin. |
| `gestion_transporte/gestion_transporte/migrations/` | Historial de estructura de la base de datos. |
| `gestion_transporte/manage.py` | Entrada administrativa de Django. |
| `gestion_transporte/run.py` | Helper para iniciar el servidor usando el puerto del `.env`. |

## Requisitos Previos

- Python 3.10 o superior.
- PostgreSQL disponible.
- Base de datos y esquema configurados.
- Entorno virtual recomendado.
- Variables de entorno configuradas en `.env`.

Variables principales:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_SCHEMA
API_PORT
```

## Puesta En Marcha

Crear y activar entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalar dependencias necesarias:

```powershell
pip install django djangorestframework django-filter djangorestframework-simplejwt drf-yasg openpyxl psycopg2-binary python-decouple
```

Ejecutar migraciones:

```powershell
python manage.py migrate
```

Crear superusuario:

```powershell
python manage.py createsuperuser
```

Iniciar servidor:

```powershell
python run.py
```

## Valor Del Proyecto

Esta API entrega una base solida para operar un sistema de transporte con criterios de seguridad, trazabilidad y escalabilidad. Sus principales fortalezas son:

- Centralizacion de informacion operativa.
- Seguridad mediante autenticacion JWT.
- Control de acceso basado en roles.
- Trazabilidad de creacion, modificacion y eliminacion.
- Eliminacion logica para proteger historicos.
- Exportacion de reportes en Excel.
- Documentacion interactiva para pruebas y presentaciones.
- Respuestas consistentes para integraciones externas.

En conjunto, el proyecto representa una solucion backend robusta para administrar recursos, operaciones y registros claves dentro de una organizacion de transporte.

| ⚠️ Advertencia |
|---------------|
| Al momento de realizar migraciones, recuerda que los campos Activo, Fecha_Creación y Fecha_Modificación, estarán por defecto como NOT NULL. Si no quieres enviar los datos al momento de realizar una operación POST, puedes configurarlos de manera manual y desactivar el valor Not Null dentro de PGAdmin. |