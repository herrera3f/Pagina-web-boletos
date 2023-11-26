from django.db import models

# Create your models here.

class Reserva(models.Model):
    nombre_y_apellido = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    numero_documento = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=255)