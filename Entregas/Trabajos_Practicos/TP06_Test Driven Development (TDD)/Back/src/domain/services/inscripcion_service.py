# Lógica de negocio para inscripciones
from sqlalchemy.orm import Session, joinedload
from src.domain.models import Actividad, Visitante, Horario, Inscripcion, crear_visitante_validado
from src.domain.exceptions import (
    CupoInsuficienteError,
    TerminosNoAceptadosError,
    HorarioNoEncontradoError,
    VisitanteNoEncontradoError,
    InscripcionDuplicadaError,
    TalleRequeridoError,
    DatosVisitantesInvalidosError
)
from typing import List, Optional
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

    def inscripcion_actividad(self, id_horario: int, id_visitante: int = None, personas: List[dict] = None, acepta_terminos: bool = True) -> List[Inscripcion]:
        """
        Realiza la inscripción de uno o múltiples visitantes a un horario de actividad.
        Puede usarse de dos formas:
        1. Individual: id_visitante=int, acepta_terminos=bool
        2. Grupal: personas=[{nombre, dni, edad, talle?}], acepta_terminos=bool
        """
        
        # Validar parámetros
        if id_visitante is None and personas is None:
            raise ValueError("Debe proporcionar id_visitante o personas")
        if id_visitante is not None and personas is not None:
            raise ValueError("No puede proporcionar ambos: id_visitante y personas")
        
        # Verificar que el horario existe
        horario = self.db.query(Horario).filter(Horario.id == id_horario).first()
        if not horario:
            raise HorarioNoEncontradoError(id_horario)

        # Verificar que el horario esté activo
        if horario.estado != "activo":
            raise ValueError(f"No se puede inscribir en un horario {horario.estado}")

        # Verificar que se acepten términos y condiciones
        if not acepta_terminos:
            raise TerminosNoAceptadosError()

        # Determinar si es individual o grupal
        if id_visitante is not None:
            # Inscripción individual
            return self._inscripcion_individual(horario, id_visitante, acepta_terminos)
        else:
            # Inscripción grupal
            return self._inscripcion_grupal(horario, personas, acepta_terminos)

    def _inscripcion_individual(self, horario: Horario, id_visitante: int, acepta_terminos: bool) -> List[Inscripcion]:
        """Maneja inscripción individual"""
        
        # Verificar cupo disponible
        cupo_disponible = horario.cupo_total - horario.cupo_ocupado
        if cupo_disponible < 1:
            raise CupoInsuficienteError(cupo_disponible, 1)

        # Verificar que el visitante existe
        visitante = self.db.query(Visitante).filter(Visitante.id == id_visitante).first()
        if not visitante:
            raise VisitanteNoEncontradoError(f"Visitante ID {id_visitante}")

        # Verificar que no esté ya inscrito
        inscripcion_existente = self.db.query(Inscripcion).filter(
            Inscripcion.id_horario == horario.id,
            Inscripcion.id_visitante == id_visitante
        ).first()
        if inscripcion_existente:
            raise InscripcionDuplicadaError(id_visitante, horario.id)

        # Verificar requerimiento de talle
        if horario.actividad.requiere_talle and not visitante.talle:
            raise TalleRequeridoError(
                id_visitante=visitante.id,
                nombre_actividad=horario.actividad.nombre
            )

        # Crear inscripción
        inscripcion = Inscripcion(
            id_horario=horario.id,
            id_visitante=id_visitante,
            nro_personas=1,
            acepta_Terminos_Condiciones=acepta_terminos
        )
        self.db.add(inscripcion)

        # Actualizar cupo
        horario.cupo_ocupado += 1
        self.db.commit()

        return [inscripcion]

    def _inscripcion_grupal(self, horario: Horario, personas: List[dict], acepta_terminos: bool) -> List[Inscripcion]:
        """Maneja inscripción grupal"""
        
        cantidad_personas = len(personas)
        
        # Verificar cupo disponible para todas las personas
        cupo_disponible = horario.cupo_total - horario.cupo_ocupado
        if cupo_disponible < cantidad_personas:
            raise CupoInsuficienteError(cupo_disponible, cantidad_personas)

        inscripciones = []
        visitantes_creados = []

        for persona in personas:
            # Buscar visitante por DNI
            visitante = self.db.query(Visitante).filter(Visitante.dni == persona['dni']).first()
            
            if not visitante:
                # Crear nuevo visitante
                try:
                    visitante = crear_visitante_validado(
                        nombre=persona['nombre'],
                        dni=persona['dni'],
                        edad=persona['edad'],
                        talle=persona.get('talle')
                    )
                    self.db.add(visitante)
                    self.db.flush()
                    visitantes_creados.append(visitante)
                except DatosVisitantesInvalidosError as e:
                    # Rollback de visitantes creados si hay error
                    for v in visitantes_creados:
                        self.db.delete(v)
                    raise ValueError(f"Datos inválidos para {persona['nombre']}: {', '.join(e.campos_faltantes)}")
            
            # Verificar que no esté ya inscrito
            inscripcion_existente = self.db.query(Inscripcion).filter(
                Inscripcion.id_horario == horario.id,
                Inscripcion.id_visitante == visitante.id
            ).first()
            if inscripcion_existente:
                # Rollback de visitantes creados si hay error
                for v in visitantes_creados:
                    self.db.delete(v)
                raise InscripcionDuplicadaError(visitante.id, horario.id)
            
            # Verificar requerimiento de talle
            if horario.actividad.requiere_talle and not visitante.talle:
                # Rollback de visitantes creados si hay error
                for v in visitantes_creados:
                    self.db.delete(v)
                raise TalleRequeridoError(
                    id_visitante=visitante.id,
                    nombre_actividad=horario.actividad.nombre
                )

            # Crear inscripción
            inscripcion = Inscripcion(
                id_horario=horario.id,
                id_visitante=visitante.id,
                nro_personas=1,
                acepta_Terminos_Condiciones=acepta_terminos
            )
            self.db.add(inscripcion)
            inscripciones.append(inscripcion)

        # Actualizar cupo
        horario.cupo_ocupado += cantidad_personas
        self.db.commit()

        return inscripciones

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
    return service.inscripcion_actividad(id_horario=id_horario, id_visitante=id_visitante, acepta_terminos=acepta_terminos)

def create_inscripcion_grupal(db: Session, id_horario: int, personas: List[dict], acepta_terminos: bool):
    """Función helper para crear inscripciones grupales"""
    service = InscripcionService(db)
    return service.inscripcion_actividad(id_horario=id_horario, personas=personas, acepta_terminos=acepta_terminos)

def get_all_inscripciones(db: Session) -> List[InscripcionConActividad]:
    """Función helper para obtener todas las inscripciones"""
    service = InscripcionService(db)
    return service.get_all_inscripciones()