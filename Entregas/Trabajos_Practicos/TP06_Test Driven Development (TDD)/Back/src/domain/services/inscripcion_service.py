# Lógica de negocio para inscripciones
from sqlalchemy.orm import Session, joinedload
from src.domain.models import Actividad, Visitante, Horario, Inscripcion
from src.domain.exceptions import (
    CupoInsuficienteError,
    TerminosNoAceptadosError,
    HorarioNoEncontradoError,
    VisitanteNoEncontradoError,
    InscripcionDuplicadaError,
    TalleRequeridoError
)
from typing import List
from pydantic import BaseModel, ConfigDict

class InscripcionConActividad(BaseModel):
    """Clase auxiliar para devolver inscripciones con nombre de actividad"""
    id: int
    id_horario: int
    id_visitante: int
    nro_personas: int
    acepta_Terminos_Condiciones: bool
    nombre_actividad: str

    model_config = ConfigDict(from_attributes=True)

class InscripcionService:
    def __init__(self, db: Session):
        self.db = db

    def inscripcion_actividad(self, id_horario: int, id_visitante: int, acepta_terminos: bool) -> Inscripcion:
        """Realiza la inscripción de un visitante individual a un horario de actividad"""

        # Verificar que el horario existe y tiene cupo disponible
        horario = self.db.query(Horario).filter(Horario.id == id_horario).first()
        if not horario:
            raise HorarioNoEncontradoError(id_horario)

        # Verificar que el horario esté activo
        if horario.estado != "activo":
            raise ValueError(f"No se puede inscribir en un horario {horario.estado}")

        # Verificar cupo disponible
        cupo_disponible = horario.cupo_total - horario.cupo_ocupado
        if cupo_disponible < 1:
            raise CupoInsuficienteError(cupo_disponible, 1)

        # Verificar que se acepten términos y condiciones
        if not acepta_terminos:
            raise TerminosNoAceptadosError()

        # Verificar que el visitante existe en la base de datos
        visitante = self.db.query(Visitante).filter(Visitante.id == id_visitante).first()
        if not visitante:
            raise VisitanteNoEncontradoError(f"Visitante ID {id_visitante}")

        # Verificar que el visitante no esté ya inscrito en este horario
        inscripcion_existente = self.db.query(Inscripcion).filter(
            Inscripcion.id_horario == id_horario,
            Inscripcion.id_visitante == id_visitante
        ).first()
        if inscripcion_existente:
            raise InscripcionDuplicadaError(id_visitante, id_horario)

        #aca arranca verificacion del test talle

        actividad = self.db.query(Actividad).filter(Actividad.id == horario.id_actividad).first()

        if actividad.requiere_talle and not visitante.talle:
            # CORRECTION: Use the instance 'actividad' to get the name string
            raise TalleRequeridoError(
                id_visitante=visitante.id,
                nombre_actividad=actividad.nombre # <-- This passes the actual string, e.g., "Tirolesa"
            )

        #aca finaliza verificacion del test  
        # Crear inscripción
        inscripcion = Inscripcion(
            id_horario=id_horario,
            id_visitante=id_visitante,
            nro_personas=1,
            acepta_Terminos_Condiciones=acepta_terminos
        )
        self.db.add(inscripcion)

        # Actualizar cupo ocupado
        horario.cupo_ocupado += 1
        self.db.commit()

        return inscripcion

    def get_all_inscripciones(self) -> List[InscripcionConActividad]:
        """Obtiene todas las inscripciones con el nombre de la actividad"""
        # Hacer join con Horario y Actividad para obtener el nombre de la actividad
        inscripciones = (
            self.db.query(Inscripcion)
            .join(Horario, Inscripcion.id_horario == Horario.id)
            .join(Actividad, Horario.id_actividad == Actividad.id)
            .options(joinedload(Inscripcion.horario).joinedload(Horario.actividad))
            .all()
        )

        # Convertir a objetos con nombre de actividad
        resultado = []
        for inscripcion in inscripciones:
            resultado.append(InscripcionConActividad(
                id=inscripcion.id,
                id_horario=inscripcion.id_horario,
                id_visitante=inscripcion.id_visitante,
                nro_personas=inscripcion.nro_personas,
                acepta_Terminos_Condiciones=inscripcion.acepta_Terminos_Condiciones,
                nombre_actividad=inscripcion.horario.actividad.nombre
            ))

        return resultado

def create_inscripcion_individual(db: Session, id_horario: int, id_visitante: int, acepta_terminos: bool):
    """Función helper para crear una inscripción individual"""
    service = InscripcionService(db)
    return service.inscripcion_actividad(id_horario, id_visitante, acepta_terminos)

def get_all_inscripciones(db: Session) -> List[InscripcionConActividad]:
    """Función helper para obtener todas las inscripciones"""
    service = InscripcionService(db)
    return service.get_all_inscripciones()