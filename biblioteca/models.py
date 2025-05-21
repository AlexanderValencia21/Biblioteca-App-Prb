from django.contrib.auth.models import AbstractUser
from django.db import models

# Opciones de rol
ROL_CHOICES = (
    ('regular', 'Usuario Regular'),
    ('admin', 'Administrador'),
)

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='regular')
    libros_prestados = models.ManyToManyField('Libro', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo', 'nombre']

    def __str__(self):
        return f"{self.username} ({self.rol})"

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio_publicacion = models.IntegerField()
    cantidad_stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
