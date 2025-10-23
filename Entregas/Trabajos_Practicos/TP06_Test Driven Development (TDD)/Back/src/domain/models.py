from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Parque(Base):
    __tablename__ = "parque"

    id = Column(Integer, primary_key=True, index=True)  # Added primary key for consistency
    horario_abrir_puertas = Column(String)
    horario_cerrar_puertas = Column(String)
    abierto = Column(Boolean)

class EstadoHorario(Base):
    __tablename__ = "estado_horario"

    nombre = Column(String, primary_key=True)
    descripcion = Column(String)

class Actividad(Base):
    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    requiere_talle = Column(Boolean)
    edad_minima = Column(Integer, nullable=True)
    descripcion = Column(String, nullable=True)

class Horario(Base):
    __tablename__ = "horario"

    id = Column(Integer, primary_key=True, index=True)
    id_actividad = Column(Integer, ForeignKey("actividad.id"))
    hora_inicio = Column(String)
    hora_fin = Column(String)
    cupo_total = Column(Integer)
    cupo_ocupado = Column(Integer)
    estado = Column(String, ForeignKey("estado_horario.nombre"))

    actividad = relationship("Actividad")
    estado_horario = relationship("EstadoHorario")

class Visitante(Base):
    __tablename__ = "visitante"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    dni = Column(Integer)
    edad = Column(Integer)
    talle = Column(String)  # Cambiado de Integer a String
    
from .exceptions import DatosVisitantesInvalidosError

TALLAS_VALIDAS = ["XS", "S", "M", "L", "XL", "XXL"]

def crear_visitante_validado(nombre: str = None, dni: int = None, edad: int = None, talle: str = None) -> Visitante:
    campos_faltantes = []

    if not nombre:
        campos_faltantes.append('nombre')
    elif not nombre.replace(' ', '').isalnum():
        campos_faltantes.append('nombre')
    if not dni:
        campos_faltantes.append('dni')
    if edad is None:
        campos_faltantes.append('edad')
    elif not isinstance(edad, int) or edad < 0 or edad > 120:
        campos_faltantes.append('edad')
    if talle is not None and talle not in TALLAS_VALIDAS:
        campos_faltantes.append('talle')
    if campos_faltantes:
        raise DatosVisitantesInvalidosError(campos_faltantes=campos_faltantes)
    return Visitante(nombre=nombre, dni=dni, edad=edad, talle=talle)

class Inscripcion(Base):
    __tablename__ = "inscripcion"

    id = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id"))
    id_visitante = Column(Integer, ForeignKey("visitante.id"))
    nro_personas = Column(Integer)
    acepta_Terminos_Condiciones = Column(Boolean)

    horario = relationship("Horario")
    visitante = relationship("Visitante")