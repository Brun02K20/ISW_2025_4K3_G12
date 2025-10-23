#!/usr/bin/env python3
"""
Script para configurar la base de datos de test
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy import create_engine, text

def setup_test_database():
    """Crear la base de datos de test si no existe"""
    try:
        # Conectar a la base de datos postgres (base de datos por defecto)
        engine = create_engine("postgresql://emmach:emma@localhost:5432/postgres")

        with engine.connect() as conn:
            # Terminar otras conexiones a la base de datos de test
            conn.execute(text("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = 'parque_db_test' AND pid <> pg_backend_pid()
            """))

            # Eliminar la base de datos si existe
            conn.execute(text("DROP DATABASE IF EXISTS parque_db_test"))

            # Crear la base de datos de test con codificación UTF-8
            conn.execute(text("CREATE DATABASE parque_db_test ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0"))

        print("✅ Base de datos de test 'parque_db_test' creada exitosamente")

    except Exception as e:
        print(f"❌ Error configurando base de datos de test: {e}")
        return False

    return True

if __name__ == "__main__":
    setup_test_database()