from django.test import TestCase
from .models import Libro, Usuario
from rest_framework.test import APIClient
from rest_framework import status

class LibroModelTest(TestCase):
    def test_crear_libro(self):
        libro = Libro.objects.create(
            titulo="Prueba",
            autor="Autor X",
            anio_publicacion=2020,
            cantidad_stock=3
        )
        self.assertEqual(libro.titulo, "Prueba")
        self.assertEqual(libro.cantidad_stock, 3)

class UsuarioLibroTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="usuario1",
            password="pass1234",
            rol="regular"
        )
        self.libro = Libro.objects.create(
            titulo="Libro Test",
            autor="Autor Test",
            anio_publicacion=2021,
            cantidad_stock=1
        )

    def test_usuario_presta_libro(self):
        self.usuario.libros_prestados.add(self.libro)
        self.assertIn(self.libro, self.usuario.libros_prestados.all())
class APILibrosTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username="admin",
            password="adminpass",
            rol="admin",
            correo="admin@test.com"
        )
        self.regular = Usuario.objects.create_user(
            username="user",
            password="userpass",
            rol="regular",
            correo="user@test.com"
        )
        self.libro = Libro.objects.create(
            titulo="API Libro",
            autor="API Autor",
            anio_publicacion=2022,
            cantidad_stock=2
        )

    def test_listar_libros(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.get('/api/libros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_libro_como_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/libros/', {
            "titulo": "Nuevo",
            "autor": "Nuevo Autor",
            "anio_publicacion": 2023,
            "cantidad_stock": 5
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_libro_como_regular(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.post('/api/libros/', {
            "titulo": "Prohibido",
            "autor": "Sin permiso",
            "anio_publicacion": 2023,
            "cantidad_stock": 5
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
