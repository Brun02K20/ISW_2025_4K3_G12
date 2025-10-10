from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Parque, ParqueCreate
from crud.parque_crud import get_parque, create_parque, update_parque

router = APIRouter(prefix="/parque", tags=["parque"])

@router.get("/", response_model=Parque)
def read_parque(db: Session = Depends(get_db)):
    parque = get_parque(db)
    if parque is None:
        raise HTTPException(status_code=404, detail="Parque not found")
    return parque

@router.post("/", response_model=Parque)
def create_parque_endpoint(parque: ParqueCreate, db: Session = Depends(get_db)):
    return create_parque(db=db, parque=parque)

@router.put("/", response_model=Parque)
def update_parque_endpoint(parque: ParqueCreate, db: Session = Depends(get_db)):
    db_parque = update_parque(db, parque=parque)
    if db_parque is None:
        raise HTTPException(status_code=404, detail="Parque not found")
    return db_parque