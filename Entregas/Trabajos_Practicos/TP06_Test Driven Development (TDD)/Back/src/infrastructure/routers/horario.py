# Endpoints para gestión de horarios
# GET /horarios/ - Listar horarios
# POST /horarios/ - Crear horario

from fastapi import APIRouter

router = APIRouter(prefix="/horarios", tags=["horarios"])

# Aquí van los endpoints de horarios