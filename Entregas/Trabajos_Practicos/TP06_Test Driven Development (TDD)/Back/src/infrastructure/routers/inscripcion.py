# Endpoints para gestión de inscripciones
# GET /inscripciones/ - Listar inscripciones
# POST /inscripciones/ - Crear inscripción

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.domain.database import get_db
from src.domain.schemas import InscripcionCreateRequest, InscripcionResponse
from src.domain.services.inscripcion_service import create_inscripcion_individual, get_all_inscripciones, InscripcionConActividad
from src.domain.exceptions import CupoInsuficienteError, TerminosNoAceptadosError, HorarioNoEncontradoError, VisitanteNoEncontradoError, InscripcionDuplicadaError

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

@router.get("/", response_model=List[InscripcionConActividad])
def read_inscripciones(db: Session = Depends(get_db)):
    """Obtener todas las inscripciones"""
    return get_all_inscripciones(db)

@router.post("/", response_model=InscripcionResponse)
def create_inscripcion_endpoint(inscripcion: InscripcionCreateRequest, db: Session = Depends(get_db)):
    """Crear una nueva inscripción individual"""
    try:
        return create_inscripcion_individual(
            db=db,
            id_horario=inscripcion.id_horario,
            id_visitante=inscripcion.id_visitante,
            acepta_terminos=inscripcion.acepta_terminos
        )
    except HorarioNoEncontradoError:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    except VisitanteNoEncontradoError:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    except CupoInsuficienteError:
        raise HTTPException(status_code=400, detail="No hay cupo disponible para este horario")
    except TerminosNoAceptadosError:
        raise HTTPException(status_code=400, detail="Debe aceptar los términos y condiciones")
    except InscripcionDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))  # 409 Conflict para duplicados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")