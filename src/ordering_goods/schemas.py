from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, constr, NonNegativeInt, Field

from src.auth.schemas import UserRead
# from src.db.models import User, ProductInfo, Category, Shop, Product


class CategoryCreate(BaseModel):
    id: int
    name: constr(max_length=40)


class CategoryRead(CategoryCreate):
    pass
    # shops: List[Any]
    # products: List[Any] = []


class CategoryUpdate(CategoryCreate):
    id: Optional[int]
    name: Optional[str]


class ShopBase(BaseModel):
    name: constr(max_length=50)


class ShopCreate(ShopBase):
    url: Optional[str] = None
    state: bool = True
    categories: List[CategoryCreate]


class ShopRead(ShopCreate):
    id: int
    user_id: Optional[int]
    # user: Optional[UserRead]
    # products_info: List["ProductInfoRead"] = []
    categories: List[CategoryCreate]


class ShopUpdate(ShopCreate):
    name: Optional[constr(max_length=50)]
    url: Optional[str]
    user_id: Optional[int]
    state: Optional[bool]


class ProductParameterCreate(BaseModel):
    value: constr(max_length=100)


class ProductParameterRead(ProductParameterCreate):
    id: int


class ParameterCreate(BaseModel):
    name: constr(max_length=40)
    product_parameters: Optional[List[ProductParameterCreate]]


class OrderItemCreate(BaseModel):
    order_id: int
    product_info_id: int
    quantity: int


class OrderItemRead(OrderItemCreate):
    id: int


class OrderItemUpdate(OrderItemCreate):
    order_id: Optional[int]
    product_info_id: Optional[int]
    quantity: Optional[int]


class ParameterRead(ParameterCreate):
    id: int
    product_parameters: List[ProductParameterRead]


class ParameterUpdate(ParameterCreate):
    name: Optional[constr(max_length=40)]


class ProductInfoCreate(BaseModel):
    model: constr(max_length=80)
    external_id: NonNegativeInt
    product_id: int
    shop_id: Optional[int]
    quantity: NonNegativeInt
    price: NonNegativeInt
    price_rrc: NonNegativeInt
    product_parameters: Optional[List[ProductParameterCreate]]
    order_items: Optional[List[OrderItemCreate]]


class ProductInfoRead(ProductInfoCreate):
    id: int
    product_parameters: List[ProductParameterRead]
    order_items: List[OrderItemRead]


class ProductInfoUpdate(ProductInfoCreate):
    model: Optional[constr(max_length=80)]
    external_id: Optional[NonNegativeInt]
    product_id: Optional[int]
    shop_id: Optional[int]
    quantity: Optional[NonNegativeInt]
    price: Optional[NonNegativeInt]
    price_rrc: Optional[NonNegativeInt]


class ProductCreate(BaseModel):
    name: constr(max_length=80)
    category_id: int
    product_info: Optional[List[ProductInfoCreate]]


class ProductRead(ProductCreate):
    id: int
    product_info: List[ProductInfoRead]


class ProductUpdate(BaseModel):
    name: Optional[constr(max_length=80)]
    category_id: Optional[int]


class OrderCreate(BaseModel):
    dt_at: datetime
    state: constr(max_length=10)
    contact_id: int
    order_items: Optional[List[OrderItemCreate]]


class OrderRead(OrderCreate):
    id: int
    order_items: List[OrderItemRead]


class OrderUpdate(OrderCreate):
    state: Optional[constr(max_length=10)]
    contact_id: Optional[int]
