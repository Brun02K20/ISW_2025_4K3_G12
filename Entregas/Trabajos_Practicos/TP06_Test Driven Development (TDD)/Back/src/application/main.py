from fastapi import FastAPI

app = FastAPI(title="API Parque de Diversiones", version="1.0.0")

from src.infrastructure.routers.inscripcion import router as inscripcion_router
app.include_router(inscripcion_router)

from src.infrastructure.routers.horario import router as horario_router
app.include_router(horario_router)

@app.get("/")
def read_root():
    return {"message": "API levantada eco parque de mierda"}