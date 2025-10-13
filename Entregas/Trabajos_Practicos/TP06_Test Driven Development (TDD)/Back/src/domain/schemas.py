from pydantic import BaseModel
from typing import Optional

# User schemas (existing)
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# Parque schemas
class ParqueBase(BaseModel):
    horario_abrir_puertas: str
    horario_cerrar_puertas: str
    abierto: bool

class ParqueCreate(ParqueBase):
    pass

class Parque(ParqueBase):
    id: int

    class Config:
        from_attributes = True

# EstadoHorario schemas
class EstadoHorarioBase(BaseModel):
    descripcion: str

class EstadoHorarioCreate(EstadoHorarioBase):
    nombre: str

class EstadoHorario(EstadoHorarioBase):
    nombre: str

    class Config:
        from_attributes = True

# Actividad schemas
class ActividadBase(BaseModel):
    nombre: str
    requiere_talle: bool

class ActividadCreate(ActividadBase):
    pass

class Actividad(ActividadBase):
    id: int

    class Config:
        from_attributes = True

# Horario schemas
class HorarioBase(BaseModel):
    hora_inicio: str
    hora_fin: str
    cupo_total: int
    cupo_ocupado: int
    estado: str

class HorarioCreate(HorarioBase):
    id_actividad: int

class Horario(HorarioBase):
    id: int
    id_actividad: int

    class Config:
        from_attributes = True

# Visitante schemas
class VisitanteBase(BaseModel):
    nombre: str
    dni: int
    edad: int
    talle: int

class VisitanteCreate(VisitanteBase):
    pass

class Visitante(VisitanteBase):
    id: int

    class Config:
        from_attributes = True

# Inscripcion schemas
class InscripcionBase(BaseModel):
    nro_personas: int
    acepta_Terminos_Condiciones: bool

class InscripcionCreate(InscripcionBase):
    id_horario: int
    id_visitante: int

class Inscripcion(InscripcionBase):
    id: int
    id_horario: int
    id_visitante: int

    class Config:
        from_attributes = True

# API schemas for Inscripcion endpoints
class InscripcionCreateRequest(BaseModel):
    id_horario: int
    id_visitante: int
    acepta_terminos: bool

class InscripcionResponse(BaseModel):
    id: int
    id_horario: int
    id_visitante: int
    nro_personas: int
    acepta_Terminos_Condiciones: bool
    nombre_actividad: str

    class Config:
        from_attributes = True