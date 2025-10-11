# Lógica de negocio para inscripciones
from sqlalchemy.orm import Session
from src.domain.models import Actividad, Visitante, Horario, Inscripcion
from src.domain.exceptions import (
    CupoInsuficienteError,
    TerminosNoAceptadosError,
    HorarioNoEncontradoError,
    VisitanteNoEncontradoError
)
from typing import List

class InscripcionService:
    def __init__(self, db: Session):
        self.db = db

    def enroll(self, id_horario: int, visitantes: List[Visitante], acepta_terminos: bool) -> Inscripcion:
        """Realiza la inscripción de visitantes a un horario de actividad"""
        # Verificar que el horario existe y tiene cupo disponible
        horario = self.db.query(Horario).filter(Horario.id == id_horario).first()
        if not horario:
            raise HorarioNoEncontradoError(id_horario)

        # Verificar cupo disponible
        cupo_disponible = horario.cupo_total - horario.cupo_ocupado
        if cupo_disponible < len(visitantes):
            raise CupoInsuficienteError(cupo_disponible, len(visitantes))

        # Verificar que se acepten términos y condiciones
        if not acepta_terminos:
            raise TerminosNoAceptadosError()

        # Crear inscripciones para cada visitante
        inscripciones = []
        for visitante in visitantes:
            # Verificar que el visitante existe en la base de datos
            visitante_db = self.db.query(Visitante).filter(Visitante.id == visitante.id).first()
            if not visitante_db:
                raise VisitanteNoEncontradoError(visitante.nombre)

            # Crear inscripción
            inscripcion = Inscripcion(
                id_horario=id_horario,
                id_visitante=visitante.id,
                nro_personas=1,  # Una inscripción por visitante
                acepta_Terminos_Condiciones=acepta_terminos
            )
            self.db.add(inscripcion)
            inscripciones.append(inscripcion)

        # Actualizar cupo ocupado
        horario.cupo_ocupado += len(visitantes)
        self.db.commit()

        # Retornar la primera inscripción como resultado representativo
        return inscripciones[0]

def create_inscripcion(db: Session, id_horario: int, visitantes: List[Visitante], acepta_terminos: bool):
    """Función helper para crear inscripciones"""
    service = InscripcionService(db)
    return service.enroll(id_horario, visitantes, acepta_terminos)