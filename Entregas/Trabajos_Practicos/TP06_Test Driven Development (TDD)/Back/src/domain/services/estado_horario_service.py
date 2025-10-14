# Lógica de negocio para estados de horario
from sqlalchemy.orm import Session
from src.domain.models import EstadoHorario
from src.domain.schemas import EstadoHorarioCreate
from typing import List

def get_estado_horario(db: Session, nombre: str) -> EstadoHorario:
    """Obtener un estado de horario por nombre"""
    return db.query(EstadoHorario).filter(EstadoHorario.nombre == nombre).first()

def get_estados_horario(db: Session) -> List[EstadoHorario]:
    """Obtener todos los estados de horario"""
    return db.query(EstadoHorario).all()

def create_estado_horario(db: Session, estado: EstadoHorarioCreate) -> EstadoHorario:
    """Crear un nuevo estado de horario"""
    db_estado = EstadoHorario(**estado.dict())
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado

def update_estado_horario(db: Session, nombre: str, estado: EstadoHorarioCreate) -> EstadoHorario:
    """Actualizar un estado de horario"""
    db_estado = db.query(EstadoHorario).filter(EstadoHorario.nombre == nombre).first()
    if db_estado:
        for key, value in estado.dict().items():
            setattr(db_estado, key, value)
        db.commit()
        db.refresh(db_estado)
    return db_estado

def delete_estado_horario(db: Session, nombre: str) -> EstadoHorario:
    """Eliminar un estado de horario"""
    db_estado = db.query(EstadoHorario).filter(EstadoHorario.nombre == nombre).first()
    if db_estado:
        db.delete(db_estado)
        db.commit()
    return db_estado