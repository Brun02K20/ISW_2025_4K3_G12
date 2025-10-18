from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Parque de Diversiones", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.infrastructure.routers.inscripcion import router as inscripcion_router
app.include_router(inscripcion_router)

from src.infrastructure.routers.horario import router as horario_router
app.include_router(horario_router)

@app.get("/")
def read_root():
    return {"message": "API levantada eco parque"}