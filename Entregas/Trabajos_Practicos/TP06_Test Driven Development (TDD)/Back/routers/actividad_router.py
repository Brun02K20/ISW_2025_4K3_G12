from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Actividad, ActividadCreate
from crud.actividad_crud import get_actividad, get_actividades, create_actividad, update_actividad, delete_actividad

router = APIRouter(prefix="/actividades", tags=["actividades"])

@router.get("/", response_model=list[Actividad])
def read_actividades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_actividades(db, skip=skip, limit=limit)

@router.get("/{actividad_id}", response_model=Actividad)
def read_actividad(actividad_id: int, db: Session = Depends(get_db)):
    actividad = get_actividad(db, actividad_id=actividad_id)
    if actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    return actividad

@router.post("/", response_model=Actividad)
def create_actividad_endpoint(actividad: ActividadCreate, db: Session = Depends(get_db)):
    return create_actividad(db=db, actividad=actividad)

@router.put("/{actividad_id}", response_model=Actividad)
def update_actividad_endpoint(actividad_id: int, actividad: ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = update_actividad(db, actividad_id=actividad_id, actividad=actividad)
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    return db_actividad

@router.delete("/{actividad_id}")
def delete_actividad_endpoint(actividad_id: int, db: Session = Depends(get_db)):
    db_actividad = delete_actividad(db, actividad_id=actividad_id)
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    return {"message": "Actividad deleted"}