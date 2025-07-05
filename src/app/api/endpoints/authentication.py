from fastapi import APIRouter
from app.services.auth_service import user_login
from app.models.login import LoginRequest

router = APIRouter()

@router.post("/login")
async def login(payload: LoginRequest):
    print('Logging in with username:', payload)
    return await user_login(payload.username, payload.password)