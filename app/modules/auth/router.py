from fastapi import APIRouter, Depends
from app.modules.auth.schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse, TokenResponse
from app.modules.auth.service import register_user, login_user
from app.core.dependencies import get_current_user
from app.modules.auth.models import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(body: RegisterRequest):
    user, token = await register_user(body)
    return AuthResponse(
        user=UserResponse(id=str(user.id), name=user.name, email=user.email),
        token=TokenResponse(access_token=token)
    )

@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    user, token = await login_user(body)
    return AuthResponse(
        user=UserResponse(id=str(user.id), name=user.name, email=user.email),
        token=TokenResponse(access_token=token)
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email
    )