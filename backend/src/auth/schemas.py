from pydantic import EmailStr, Field
from src.models import CustomModel


class AuthUser(CustomModel):
    email: EmailStr
    username: str
    image: str


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserResponse(CustomModel):
    email: EmailStr
