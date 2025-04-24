from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, conlist

from models import User


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=6)
    phone_number: Optional[str] = None
    role_id: int


def to_User(user: BaseModel):
    return User(**user.model_dump())


class UserResponse(BaseModel):
    id: int
    role_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    phone_number: Optional[str]
    is_superuser: bool
    is_admin: bool
    avatar: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class RoleCreate(BaseModel):
    name: str
    permissions: conlist(str, min_length=1)


class RoleUpdate(RoleCreate):
    pass
