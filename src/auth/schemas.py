from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role_id: int

    class Config:
        # orm_mode = True #old Version
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    role_id: int
