from typing import NewType, Optional

from pydantic import BaseModel, EmailStr, Field

from models import User


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


LoggedInUser = NewType("LoggedInUser", User)


class TokenUserPayload(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_admin: bool
    role: Optional[str]
    permissions: Optional[list[str]]
