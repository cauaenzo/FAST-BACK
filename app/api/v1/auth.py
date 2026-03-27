from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    """Autentica o usuário e retorna o token JWT."""
    user = await UserRepository(session).find_by_username(data.username)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return TokenResponse(access_token=create_access_token({"sub": user.username, "role": user.role}))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    """Registra um novo usuário com role padrão (user)."""
    repo = UserRepository(session)
    if await repo.find_by_username(data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuário já existe")
    user = User(username=data.username, password=hash_password(data.password), role=UserRole.USER)
    return await repo.save(user)
