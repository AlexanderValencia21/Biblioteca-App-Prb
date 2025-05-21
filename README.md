# Biblioteca App – Prueba Técnica Backend

Aplicación desarrollada como parte de una prueba técnica para el rol de desarrollador backend.

Permite gestionar libros, usuarios, préstamos y devoluciones. Incluye vistas web, autenticación, y una API REST con permisos basados en roles.

---

## Tecnologías utilizadas

- Python 3.13
- Django 5.2
- Django REST Framework
- SQLite (desarrollo) / PostgreSQL (deploy)
- JWT para autenticación
- Bootstrap (frontend básico)
- Postman (para pruebas de la API)

---

## Funcionalidades principales

### Web

- Listar libros y ver detalles
- Crear y editar libros (solo admin)
- Tomar y devolver libros (solo usuarios regulares)
- Acceso diferenciado por rol (`admin` y `regular`)
- Interfaz de administración de Django


### API REST (vía DRF)

| Método | Endpoint                         | Acceso              | Descripción                   |
|--------|----------------------------------|---------------------|-------------------------------|
| POST   | `/api/token/`                    | Público             | Obtener tokens JWT            |
| GET    | `/api/libros/`                   | Autenticado         | Listar libros                 |
| GET    | `/api/libros/{id}/`              | Autenticado         | Detalle de libro              |
| POST   | `/api/libros/`                   | Admin               | Crear libro                   |
| PUT    | `/api/libros/{id}/`              | Admin               | Editar libro                  |
| DELETE | `/api/libros/{id}/`              | Admin               | Eliminar libro                |
| POST   | `/api/libros/{id}/prestar/`      | Usuario regular     | Tomar prestado un libro       |
| POST   | `/api/libros/{id}/devolver/`     | Usuario regular     | Devolver un libro             |


## Pruebas automatizadas

Incluye pruebas unitarias para:

- Modelos (`Libro`, `Usuario`)
- API REST (listado, permisos, préstamos)
- Lógica de negocio de préstamo/devolución

```bash
python manage.py test
```

## Uso de la aplicacion (LOCAL)

Clonar el repositorio:
```bash
git clone https://github.com/AlexanderValencia21/Biblioteca-App-Prb.git
```
Navegar hasta la carpeta del repositorio y crear un Virtual Env

```bash
python -m venv venv
venv\Scripts\activate #Linux: source venv/bin/activate 
pip install -r requirements.txt
```

Ejecutar migraciones y servidor:

```bash
python manage.py migrate
python manage.py runserver
```

Después de ejecutar las migraciones, hay que crear un superusuario para ingresar al panel de administración:

```bash
python manage.py createsuperuser
```
y en el panel de administracion crear un usuario regular y cambiar el rol del super usuario a Administrador, colocar `/admin` en la url local para entrar al panel de administracion

## Uso de la aplicacion (En la Nube)

Navegar al link : https://biblioteca-app-prb.onrender.com/login/

- Para ingresar ya hay un usuario con permisos de admin, las credenciales son `admin` y `admin123`, usuario y contraseña respectivamente.
- El usuario con permisos regulares es `user1` y `usuario1`,usuario y contraseña respectivamente

Para las peticiones de la API hay una carpeta llamada postman donde hay un archivo que se puede importar en postman y hacer las peticiones

Hay que iniciar sesion en la carpeta `AUTH`con la request que ahi se ecuentra, con las credenciales ya sea de `admin` o de `user1`, para obtener el token de autenticacion y poder probar todas las request 

Cuerpo para crear o editar un libro, por si no aparece en la coleccion.
``` bash
{
  "titulo": "Betty la seria",
  "autor": "Daniel",
  "anio_publicacion": 2010,
  "cantidad_stock": 10
}
```
