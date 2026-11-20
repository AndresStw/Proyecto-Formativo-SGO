from fastapi import APIRouter

from app.api.v1.auth import router as auth_router


api_router = APIRouter()
api_router.include_router(auth_router)

# En las siguientes fases registraremos aquí los routers de:
# auth, clientes, empleados, procedimientos, citas, tratamientos, etc.