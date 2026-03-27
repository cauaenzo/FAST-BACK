from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.core.database import get_session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, PasswordUpdate, RolePatch, TokenResponse, UserListResponse, UserResponse

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


@router.get("/users", response_model=UserListResponse)
async def list_users(
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
):
    """Lista todos os usuários. Requer admin."""
    users = await UserRepository(session).find_all()
    return UserListResponse(total=len(users), users=users)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Busca um usuário por ID. Admin pode buscar qualquer um, user só o próprio."""
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    user = await UserRepository(session).find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/users/{user_id}/password", response_model=UserResponse)
async def update_password(
    user_id: int,
    data: PasswordUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Atualiza a senha do usuário. Cada usuário só pode alterar a própria senha."""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você só pode alterar sua própria senha")
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha atual incorreta")
    current_user.password = hash_password(data.new_password)
    return await UserRepository(session).save(current_user)


@router.patch("/users/{user_id}/role", response_model=UserResponse)
async def update_role(
    user_id: int,
    data: RolePatch,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_admin),
):
    """Promove ou rebaixa o role de um usuário. Requer admin."""
    repo = UserRepository(session)
    user = await repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.role = data.role
    return await repo.save(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    """Remove um usuário. Requer admin. Admin não pode deletar a si mesmo."""
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin não pode deletar a si mesmo")
    repo = UserRepository(session)
    user = await repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await repo.delete(user_id)
