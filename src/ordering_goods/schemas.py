from typing import Optional, List

from sqlmodel import SQLModel, Field

from src.db.models import User, ProductInfo, Category, Shop, Product


class ShopCreate(SQLModel):
    name: str = Field(max_length=50, unique=True)
    url: Optional[str] = None
    state: bool = True


class ShopRead(ShopCreate):
    id: int
    user: Optional[User] = None
    products_info: List[ProductInfo] = []
    categories: List[Category] = []


class ShopUpdate(ShopCreate):
    name: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    state: Optional[bool] = None


class CategoryCreate(SQLModel):
    id: Optional[int] = None
    name: str = Field(max_length=40, unique=True)
    shops_id: List[int] = []


class CategoryRead(CategoryCreate):
    id: int
    shops: List[Shop] = []
    products: List[Product] = []


class CategoryUpdate(CategoryCreate):
    name: Optional[str] = None
    shops_id: List[int] = []
