# Lógica de negocio para actividades
from sqlalchemy.orm import Session
from src.domain.models import Actividad
from src.domain.schemas import ActividadCreate

def get_actividades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Actividad).offset(skip).limit(limit).all()

def get_actividad(db: Session, actividad_id: int):
    return db.query(Actividad).filter(Actividad.id == actividad_id).first()

def create_actividad(db: Session, actividad: ActividadCreate):
    db_actividad = Actividad(
        nombre=actividad.nombre,
        requiere_talle=actividad.requiere_talle,
        edad_minima=actividad.edad_minima,
        descripcion=actividad.descripcion
    )
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

def update_actividad(db: Session, actividad_id: int, actividad: ActividadCreate):
    db_actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if db_actividad:
        db_actividad.nombre = actividad.nombre
        db_actividad.requiere_talle = actividad.requiere_talle
        db_actividad.edad_minima = actividad.edad_minima
        db_actividad.descripcion = actividad.descripcion
        db.commit()
        db.refresh(db_actividad)
    return db_actividad

def delete_actividad(db: Session, actividad_id: int):
    db_actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if db_actividad:
        db.delete(db_actividad)
        db.commit()
    return db_actividad