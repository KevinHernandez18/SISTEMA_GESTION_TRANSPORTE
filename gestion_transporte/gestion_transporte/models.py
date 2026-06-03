from django.db import models

# Create your models here.

class conductores(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    licencia = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'conductores'

class vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20)
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

class estaciones(models.Model):
    id_estacion = models.AutoField(primary_key=True)
    nombre_estacion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_estacion
    
    class Meta:
        db_table = 'estaciones'

class rutas(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre_ruta = models.CharField(max_length=100)
    id_origen = models.ForeignKey(
        estaciones,
        on_delete=models.CASCADE,
        db_column='id_estacion',
        related_name='origen_estacion'
    )
    id_destino = models.ForeignKey(
        estaciones,
        on_delete=models.CASCADE,
        db_column='id_estacion',
        related_name='destino_estacion'
        )
    distancia_km = models.FloatField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_ruta
    
    class Meta:
        db_table = 'rutas'
    
class viajes(models.Model):
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
        return f'Viaje {self.id_viaje} - Conductor: {self.id_conductor.nombre} - Vehículo: {self.id_vehiculo.placa} - Ruta: {self.id_ruta.nombre_ruta}'
    
    class Meta:
        db_table = 'viajes'

class pasajeros(models.Model):
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
    
class boletos(models.Model):
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
        return f'Boleto {self.id_boleto} - Pasajero: {self.id_pasajero.nombre} - Viaje: {self.id_viaje.id_viaje}'
    
    class Meta:
        db_table = 'boletos'

class mantenimientos(models.Model):
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
        return f'Mantenimiento {self.id_mantenimiento} - Vehículo: {self.id_vehiculo.placa} - Fecha: {self.fecha_mantenimiento.strftime("%Y-%m-%d")}'
    
    class Meta:
        db_table = 'mantenimientos'