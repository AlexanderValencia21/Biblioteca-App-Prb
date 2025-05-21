#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit

# Ejecutar migraciones y recolectar archivos estáticos
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate