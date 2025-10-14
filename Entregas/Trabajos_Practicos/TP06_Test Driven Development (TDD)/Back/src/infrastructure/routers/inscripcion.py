# Endpoints para gestión de inscripciones
# GET /inscripciones/ - Listar inscripciones
# GET /inscripciones/con-visitantes - Listar inscripciones con datos de visitantes
# POST /inscripciones/ - Crear inscripción (individual o grupal)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.domain.database import get_db
from src.domain.schemas import InscripcionUnificadaCreateRequest, InscripcionConVisitantes
from src.domain.services.inscripcion_service import create_inscripcion_unificada, get_all_inscripciones, get_all_inscripciones_con_visitantes, InscripcionConActividad
from src.domain.services.inscripcion_service import create_inscripcion_unificada, get_all_inscripciones, InscripcionConActividad
from src.domain.exceptions import CupoInsuficienteError, TerminosNoAceptadosError, HorarioNoEncontradoError, VisitanteNoEncontradoError, InscripcionDuplicadaError, TalleRequeridoError

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

@router.get("/", response_model=List[InscripcionConActividad])
def read_inscripciones(db: Session = Depends(get_db)):
    """Obtener todas las inscripciones"""
    return get_all_inscripciones(db)

@router.get("/con-visitantes", response_model=List[InscripcionConVisitantes])
def read_inscripciones_con_visitantes(db: Session = Depends(get_db)):
    """Obtener todas las inscripciones con datos completos de los visitantes"""
    return get_all_inscripciones_con_visitantes(db)

@router.post("/", response_model=List[InscripcionConActividad])
def create_inscripcion_endpoint(inscripcion: InscripcionUnificadaCreateRequest, db: Session = Depends(get_db)):
    """Crear inscripción individual o grupal"""
    try:
        # Convertir visitantes a formato dict para el servicio
        visitantes_dict = [
            {
                "nombre": v.nombre,
                "dni": v.dni,
                "edad": v.edad,
                "talle": v.talle
            }
            for v in inscripcion.visitantes
        ]
        
        inscripciones = create_inscripcion_unificada(
            db=db,
            id_horario=inscripcion.id_horario,
            visitantes=visitantes_dict,
            acepta_terminos=inscripcion.acepta_terminos
        )
        
        # Convertir a formato de respuesta
        resultado = []
        for insc in inscripciones:
            resultado.append(InscripcionConActividad(
                id=insc.id,
                id_horario=insc.id_horario,
                id_visitante=insc.id_visitante,
                nro_personas=insc.nro_personas,
                acepta_Terminos_Condiciones=insc.acepta_Terminos_Condiciones,
                nombre_actividad=insc.horario.actividad.nombre
            ))
        
        return resultado
        
    except HorarioNoEncontradoError:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    except VisitanteNoEncontradoError:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    except CupoInsuficienteError:
        raise HTTPException(status_code=400, detail="No hay cupo disponible")
    except TerminosNoAceptadosError:
        raise HTTPException(status_code=400, detail="Debe aceptar los términos y condiciones")
    except InscripcionDuplicadaError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TalleRequeridoError as e:
        raise HTTPException(status_code=400, detail=f"La actividad {e.nombre_actividad} requiere talle pero el visitante no lo tiene asignado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")