# Endpoints para gestión de inscripciones
# GET /inscripciones/ - Listar inscripciones
# POST /inscripciones/ - Crear inscripción

from fastapi import APIRouter

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

# Aquí van los endpoints de inscripciones