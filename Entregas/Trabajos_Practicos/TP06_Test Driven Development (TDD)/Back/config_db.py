import os
# config.py

# Constantes de configuración para la base de datos

USUARIO_DB = os.getenv("DB_USER", "postgres")
CONTRASENA_DB = os.getenv("DB_PASSWORD", "admin")
URL_DB = os.getenv("DB_HOST", "localhost")
PUERTO_DB = os.getenv("DB_PORT", "5432")
DATABASE_NAME = os.getenv("DB_NAME", "parque_db")