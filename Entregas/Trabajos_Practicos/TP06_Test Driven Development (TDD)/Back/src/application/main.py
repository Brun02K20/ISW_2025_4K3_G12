from fastapi import FastAPI

app = FastAPI(title="API Parque de Diversiones", version="1.0.0")

# Aquí incluir los routers cuando estén implementados
# from src.infrastructure.routers import parque, actividad
# app.include_router(parque.router)
# app.include_router(actividad.router)
# etc.

# Incluir router de inscripciones
from src.infrastructure.routers.inscripcion import router as inscripcion_router
app.include_router(inscripcion_router)

@app.get("/")
def read_root():
    return {"message": "API levantada eco parque de mierda"}