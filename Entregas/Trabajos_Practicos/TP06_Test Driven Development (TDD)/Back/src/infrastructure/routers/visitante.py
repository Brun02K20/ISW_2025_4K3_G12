# Endpoints para gestión de visitantes
# GET /visitantes/ - Listar visitantes
# POST /visitantes/ - Crear visitante

from fastapi import APIRouter

router = APIRouter(prefix="/visitantes", tags=["visitantes"])

# Aquí van los endpoints de visitantes