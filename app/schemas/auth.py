from pydantic import BaseModel, Field

from app.models.user import UserRole


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    users: list[UserResponse]


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)


class RolePatch(BaseModel):
    role: UserRole
