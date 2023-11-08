from datetime import datetime

from pydantic import EmailStr, Field
from src.models import CustomModel


class AuthUser(CustomModel):
    email: EmailStr
    username: str
    image: str
    token: str


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserResponse(CustomModel):
    id: int
    email: EmailStr
    username: str | None
    image: str | None
    is_admin: bool
    created_at: datetime | None
