from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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
    talle = Column(Integer)

class Inscripcion(Base):
    __tablename__ = "inscripcion"

    id = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey("horario.id"))
    id_visitante = Column(Integer, ForeignKey("visitante.id"))
    nro_personas = Column(Integer)
    acepta_Terminos_Condiciones = Column(Boolean)

    horario = relationship("Horario")
    visitante = relationship("Visitante")