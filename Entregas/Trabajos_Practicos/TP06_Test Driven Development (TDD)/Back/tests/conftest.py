# Configuración de fixtures para tests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.domain.database import Base, get_db
from src.application.main import app

TEST_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/parque_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Limpiar todas las tablas antes del test
    with engine.connect() as conn:
        # Deshabilitar restricciones de clave foránea temporalmente
        conn.execute(text("SET session_replication_role = 'replica'"))
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"DELETE FROM {table.name}"))
        # Rehabilitar restricciones de clave foránea
        conn.execute(text("SET session_replication_role = 'origin'"))
        conn.commit()

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Revertir cambios después de cada test
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture para crear un cliente de test de FastAPI"""
    # Override the dependency to use our test database session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client