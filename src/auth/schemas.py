from typing import Optional, Literal, List
from pydantic import EmailStr

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    company: str
    position: str
    username: str
    usertype: Literal["shop", "buyer"]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    company: Optional[str]
    position: Optional[str]
    username: str
    usertype: Literal["shop", "buyer"] = "buyer"
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    shop: Optional["Shop"] = None
    contacts: List["Contact"] = []
    orders: List["Order"] = []


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    email: Optional[EmailStr]
    company: Optional[str]
    position: Optional[str]
    username: Optional[str]
    usertype: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
