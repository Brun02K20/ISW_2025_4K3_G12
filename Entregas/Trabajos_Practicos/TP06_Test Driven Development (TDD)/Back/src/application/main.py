from fastapi import FastAPI

app = FastAPI(title="API Parque de Diversiones", version="1.0.0")

# Aquí incluir los routers cuando estén implementados
# from src.infrastructure.routers import parque, actividad
# app.include_router(parque.router)
# app.include_router(actividad.router)
# etc.

@app.get("/")
def read_root():
    return {"message": "API levantada eco parque de mierda"}