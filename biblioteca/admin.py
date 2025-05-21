from django.contrib import admin
from .models import Libro, Usuario
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'correo', 'rol']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('nombre', 'correo', 'rol', 'libros_prestados')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Libro)
