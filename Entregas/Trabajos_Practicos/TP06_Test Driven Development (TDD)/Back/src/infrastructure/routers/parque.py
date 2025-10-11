# Endpoints para gestión del parque
# GET /parque/ - Obtener información del parque
# PUT /parque/ - Actualizar estado del parque

from fastapi import APIRouter

router = APIRouter(prefix="/parque", tags=["parque"])

# Aquí van los endpoints del parque