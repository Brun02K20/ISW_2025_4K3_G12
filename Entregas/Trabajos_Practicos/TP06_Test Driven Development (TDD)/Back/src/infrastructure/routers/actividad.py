# Endpoints para gestión de actividades
# GET /actividades/ - Listar actividades
# POST /actividades/ - Crear actividad

from fastapi import APIRouter

router = APIRouter(prefix="/actividades", tags=["actividades"])

# Aquí van los endpoints de actividades