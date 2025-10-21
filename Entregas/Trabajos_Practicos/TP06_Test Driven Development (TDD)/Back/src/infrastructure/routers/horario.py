
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, ConfigDict
from typing import List
from src.domain.database import get_db
from src.domain.models import Horario, Actividad, EstadoHorario

router = APIRouter(prefix="/horarios", tags=["horarios"])

class HorarioConDetalles(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_actividad: int
    hora_inicio: str
    hora_fin: str
    cupo_total: int
    cupo_ocupado: int
    estado: str
    
    actividad: dict  # Contendrá id, nombre, requiere_talle
    
    estado_horario: dict  # Contendrá nombre, descripcion

@router.get("/", response_model=List[HorarioConDetalles])
def get_horarios(db: Session = Depends(get_db)):
    """
    Obtener todos los horarios con información completa de actividad y estado_horario
    """
    horarios = (
        db.query(Horario)
        .options(joinedload(Horario.actividad))
        .options(joinedload(Horario.estado_horario))
        .all()
    )
    
    # Convertir a formato de respuesta
    result = []
    for h in horarios:
        result.append(HorarioConDetalles(
            id=h.id,
            id_actividad=h.id_actividad,
            hora_inicio=h.hora_inicio,
            hora_fin=h.hora_fin,
            cupo_total=h.cupo_total,
            cupo_ocupado=h.cupo_ocupado,
            estado=h.estado,
            actividad={
                "id": h.actividad.id,
                "nombre": h.actividad.nombre,
                "requiere_talle": h.actividad.requiere_talle,
                "edad": h.actividad.edad_minima,
                "descripcion": h.actividad.descripcion
            },
            estado_horario={
                "nombre": h.estado_horario.nombre,
                "descripcion": h.estado_horario.descripcion
            }
        ))
    
    return result