from django.db import models
from django.core.exceptions import ValidationError

from .mixins import AuditableModel, AuditLog

# Create your models here.

class conductores(AuditableModel):
    id_conductor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'conductores'

class vehiculos(AuditableModel):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.placa
    
    class Meta:
        db_table = 'vehiculos'

class estaciones(AuditableModel):
    id_estacion = models.AutoField(primary_key=True)
    nombre_estacion = models.CharField(max_length=100, unique=True)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_estacion
    
    class Meta:
        db_table = 'estaciones'

class rutas(AuditableModel):
    id_ruta = models.AutoField(primary_key=True)
    nombre_ruta = models.CharField(max_length=100, unique=True)
    id_origen = models.ForeignKey(
        estaciones,
        on_delete=models.CASCADE,
        db_column='id_origen',
        related_name='origen_estacion'
    )
    id_destino = models.ForeignKey(
        estaciones,
        on_delete=models.CASCADE,
        db_column='id_destino',
        related_name='destino_estacion'
        )
    distancia_km = models.FloatField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_ruta

    def clean(self):
        if self.id_origen_id and self.id_destino_id and self.id_origen_id == self.id_destino_id:
            raise ValidationError('La estacion de origen no puede ser la misma que la estacion de destino.')
    
    class Meta:
        db_table = 'rutas'
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(id_origen=models.F('id_destino')),
                name='origen_destino_diferentes'
            )
        ]
    
class viajes(AuditableModel):
    id_viaje = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(
        vehiculos,
        on_delete=models.CASCADE,
        db_column='id_vehiculo'
        )
    id_conductor = models.ForeignKey(
        conductores,
        on_delete=models.CASCADE,
        db_column='id_conductor'
        )
    id_ruta = models.ForeignKey(
        rutas,
        on_delete=models.CASCADE,
        db_column='id_ruta')
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Viaje {self.id_viaje}'
    
    class Meta:
        db_table = 'viajes'

class pasajeros(AuditableModel):
    id_pasajero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'pasajeros'
    
class boletos(AuditableModel):
    id_boleto = models.AutoField(primary_key=True)
    id_viaje = models.ForeignKey(
        viajes,
        on_delete=models.CASCADE,
        db_column='id_viaje'
        )
    id_pasajero = models.ForeignKey(
        pasajeros,
        on_delete=models.CASCADE,
        db_column='id_pasajero'
        )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Boleto {self.id_boleto}'
    
    class Meta:
        db_table = 'boletos'

class mantenimientos(AuditableModel):
    id_mantenimiento = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(
        vehiculos,
        on_delete=models.CASCADE,
        db_column='id_vehiculo'
        )
    descripcion = models.TextField()
    fecha_mantenimiento = models.DateTimeField()
    costo = models.FloatField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Mantenimiento {self.id_mantenimiento}'
    
    class Meta:
        db_table = 'mantenimientos'


class licencia(AuditableModel):
    id_licencia = models.AutoField(primary_key=True)
    id_conductor = models.ForeignKey(
        conductores,
        on_delete=models.CASCADE,
        db_column='id_conductor'
        )
    numero_licencia = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Licencia {self.numero_licencia}'
    
    class Meta:
        db_table = 'licencia'

class documentos(AuditableModel):
    id_documento = models.AutoField(primary_key=True)
    id_conductor = models.ForeignKey(
        conductores,
        on_delete=models.CASCADE,
        db_column='id_conductor'
    )
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField()
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Documento {self.tipo_documento}'
    
    class Meta:
        db_table = 'documentos'
