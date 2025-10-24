from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from config_db import USUARIO_DB, CONTRASENA_DB, PUERTO_DB, URL_DB, DATABASE_NAME

# Database configuration with proper encoding
DATABASE_URL = f"postgresql://{USUARIO_DB}:{CONTRASENA_DB}@{URL_DB}:{PUERTO_DB}/{DATABASE_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    pool_pre_ping=True,  # Verify connections before use
    connect_args={
        "client_encoding": "utf8",
        "options": "-c timezone=UTC"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()