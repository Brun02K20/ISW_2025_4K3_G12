from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.domain.database import get_db
from src.domain.schemas import EstadoHorario, EstadoHorarioCreate
from src.domain.services.estado_horario_service import get_estado_horario, get_estados_horario, create_estado_horario, update_estado_horario, delete_estado_horario

router = APIRouter(prefix="/estados-horario", tags=["estados_horario"])

@router.get("/", response_model=list[EstadoHorario])
def read_estados_horario(db: Session = Depends(get_db)):
    return get_estados_horario(db)

@router.get("/{nombre}", response_model=EstadoHorario)
def read_estado_horario(nombre: str, db: Session = Depends(get_db)):
    estado = get_estado_horario(db, nombre=nombre)
    if estado is None:
        raise HTTPException(status_code=404, detail="EstadoHorario not found")
    return estado

@router.post("/", response_model=EstadoHorario)
def create_estado_horario_endpoint(estado: EstadoHorarioCreate, db: Session = Depends(get_db)):
    return create_estado_horario(db=db, estado=estado)

@router.put("/{nombre}", response_model=EstadoHorario)
def update_estado_horario_endpoint(nombre: str, estado: EstadoHorarioCreate, db: Session = Depends(get_db)):
    db_estado = update_estado_horario(db, nombre=nombre, estado=estado)
    if db_estado is None:
        raise HTTPException(status_code=404, detail="EstadoHorario not found")
    return db_estado

@router.delete("/{nombre}")
def delete_estado_horario_endpoint(nombre: str, db: Session = Depends(get_db)):
    db_estado = delete_estado_horario(db, nombre=nombre)
    if db_estado is None:
        raise HTTPException(status_code=404, detail="EstadoHorario not found")
    return {"message": "EstadoHorario deleted"}