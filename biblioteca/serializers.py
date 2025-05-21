from rest_framework import serializers
from .models import Libro, Usuario

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    libros_prestados = LibroSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'correo', 'rol', 'libros_prestados']
