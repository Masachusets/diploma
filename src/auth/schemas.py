from typing import Optional, Literal, List, Any
from pydantic import EmailStr, BaseModel, constr

from fastapi_users import schemas


class ContactBase(BaseModel):
    city: constr(max_length=50)
    street: constr(max_length=100)
    house: constr(max_length=15)
    structure: constr(max_length=15)
    building: constr(max_length=15)
    apartment: constr(max_length=15)
    phone: constr(max_length=50)


class ContactCreate(ContactBase):
    user_id: Optional[int]


class ContactRead(ContactBase):
    id: int


class ContactUpdate(ContactCreate):
    city: Optional[constr(max_length=50)]
    street: Optional[constr(max_length=100)]
    house: Optional[constr(max_length=15)]
    structure: Optional[constr(max_length=15)]
    building: Optional[constr(max_length=15)]
    apartment: Optional[constr(max_length=15)]
    phone: Optional[constr(max_length=50)]


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    company: str
    position: str
    username: str
    usertype: Literal["buyer", "shop"]  # UserTypeEnum
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    # shop: Optional[Any]  # Optional["Shop"] = None
    # contacts: Optional[List[ContactRead]]
    # orders: list

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    company: Optional[str]
    position: Optional[str]
    username: str
    usertype: Literal["buyer", "shop"] = "buyer"
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    # shop: Optional["Shop"] = None
    # contacts: List["Contact"] = []
    # orders: List["Order"] = []


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    email: Optional[EmailStr]
    company: Optional[str]
    position: Optional[str]
    username: Optional[str]
    usertype: Optional[Literal["buyer", "shop"]]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
    # contacts: Optional[List[ContactUpdate]]
