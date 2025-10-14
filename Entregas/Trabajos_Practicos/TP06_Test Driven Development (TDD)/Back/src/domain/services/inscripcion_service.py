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
from src.domain.schemas import VisitanteInfo, InscripcionConVisitantes

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

    def inscripcion_actividad(self, id_horario: int, visitantes: List[dict], acepta_terminos: bool = True) -> List[Inscripcion]:
        """
        Realiza la inscripción de uno o múltiples visitantes a un horario de actividad.
        visitantes: lista de dicts con {nombre, dni, edad, talle?}
        """
        
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

        cantidad_personas = len(visitantes)
        
        # Verificar cupo disponible para todas las personas
        cupo_disponible = horario.cupo_total - horario.cupo_ocupado
        if cupo_disponible < cantidad_personas:
            raise CupoInsuficienteError(cupo_disponible, cantidad_personas)

        inscripciones = []
        visitantes_creados = []

        for persona in visitantes:
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

    def get_all_inscripciones_con_visitantes(self) -> List[InscripcionConVisitantes]:
        """Obtiene todas las inscripciones con el nombre de la actividad y datos del visitante"""
        # Hacer join con Horario, Actividad y Visitante para obtener toda la información
        inscripciones = (
            self.db.query(Inscripcion)
            .join(Horario, Inscripcion.id_horario == Horario.id)
            .join(Actividad, Horario.id_actividad == Actividad.id)
            .join(Visitante, Inscripcion.id_visitante == Visitante.id)
            .options(
                joinedload(Inscripcion.horario).joinedload(Horario.actividad),
                joinedload(Inscripcion.visitante)
            )
            .all()
        )

        # Convertir a objetos con nombre de actividad y datos del visitante
        resultado = []
        for inscripcion in inscripciones:
            resultado.append(InscripcionConVisitantes(
                id=inscripcion.id,
                id_horario=inscripcion.id_horario,
                nro_personas=inscripcion.nro_personas,
                acepta_Terminos_Condiciones=inscripcion.acepta_Terminos_Condiciones,
                nombre_actividad=inscripcion.horario.actividad.nombre,
                visitante=VisitanteInfo(
                    id=inscripcion.visitante.id,
                    nombre=inscripcion.visitante.nombre,
                    dni=inscripcion.visitante.dni,
                    edad=inscripcion.visitante.edad,
                    talle=inscripcion.visitante.talle
                )
            ))

        return resultado

def create_inscripcion_unificada(db: Session, id_horario: int, visitantes: List[dict], acepta_terminos: bool = True):
    """Función helper unificada para crear inscripciones"""
    service = InscripcionService(db)
    return service.inscripcion_actividad(id_horario=id_horario, visitantes=visitantes, acepta_terminos=acepta_terminos)

def create_inscripcion_individual(db: Session, id_horario: int, id_visitante: int, acepta_terminos: bool):
    """Función helper para crear una inscripción individual - busca el visitante por ID"""
    service = InscripcionService(db)
    visitante = service.db.query(Visitante).filter(Visitante.id == id_visitante).first()
    if not visitante:
        raise VisitanteNoEncontradoError(f"Visitante ID {id_visitante}")
    
    # Convertir a formato de lista
    visitantes = [{
        'nombre': visitante.nombre,
        'dni': visitante.dni,
        'edad': visitante.edad,
        'talle': visitante.talle
    }]
    
    return service.inscripcion_actividad(id_horario=id_horario, visitantes=visitantes, acepta_terminos=acepta_terminos)

def create_inscripcion_grupal(db: Session, id_horario: int, personas: List[dict], acepta_terminos: bool):
    """Función helper para crear inscripciones grupales"""
    service = InscripcionService(db)
    return service.inscripcion_actividad(id_horario=id_horario, visitantes=personas, acepta_terminos=acepta_terminos)

def get_all_inscripciones(db: Session) -> List[InscripcionConActividad]:
    """Función helper para obtener todas las inscripciones"""
    service = InscripcionService(db)
    return service.get_all_inscripciones()

def get_all_inscripciones_con_visitantes(db: Session) -> List[InscripcionConVisitantes]:
    """Función helper para obtener todas las inscripciones con datos de visitantes"""
    service = InscripcionService(db)
    return service.get_all_inscripciones_con_visitantes()