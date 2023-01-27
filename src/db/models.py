from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlmodel import Field, Relationship, SQLModel

Base = declarative_base()


class UserEnum(str, Enum):
    BUYER = "buyer"
    SHOP = "shop"


class OrderEnum(str, Enum):
    BASKET = "basket"
    NEW = "new"
    CONFIRMED = "confirmed"
    ASSEMBLED = "assembled"
    SENT = "sent"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email: EmailStr = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    company: str = Column(String(length=40), default=None)
    position: str = Column(String(length=40), default=None)
    username: str = Column(String(length=150), unique=True)
    usertype: UserEnum = Column(String(length=5), default="buyer")
    shop: "Shop" = relationship("Shop", back_populates="user")
    contacts: List["Contact"] = relationship("Contact", back_populates="user")
    orders: List["Order"] = relationship("Order", back_populates="user")


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):

    @declared_attr
    def user_id(cls):
        return Field(foreign_key="user.id", nullable=False)


class ShopCategoryLink(Base):

    __tablename__ = "shop_category"

    shop_id: int = Column("shop_id", ForeignKey("shop.id"))
    category_id: int = Column("category_id", ForeignKey("category.id"))


class Shop(Base):

    __tablename__ = "shop"

    id: Optional[int] = Column(Integer, primary_key=True)
    name: str = Column(String(length=50))
    url: str = Column(String)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    user: "User" = relationship("User", back_populates="shop")
    state: bool = Column(Boolean, default=True)
    products_info: List["ProductInfo"] = relationship("ProductInfo", back_populates="shop")
    categories: List["Category"] = relationship("Category", secondary=ShopCategoryLink)


class Category(Base):

    __tablename__ = "category"

    id: Optional[int] = Column(Integer, primary_key=True)
    name: str = Column(String(length=40), unique=True)
    shops: List["Shop"] = relationship("Shop", secondary=ShopCategoryLink)
    products: List["Product"] = relationship("Product", back_populates="category")


class Product(SQLModel, table=True):

    __tablename__ = "product"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(max_length=80)
    category_id: Optional[int] = Field(foreign_key="category.id")
    product_info: List["ProductInfo"] = Relationship(back_populates="product")


class ProductInfo(SQLModel, table=True):

    __tablename__ = "product_info"

    id: Optional[int] = Field(primary_key=True)
    model: Optional[str] = Field(max_length=80)
    external_id: int = Field(ge=0)
    product_id: Optional[int] = Field(foreign_key="product.id")
    shop_id: Optional[int] = Field(foreign_key="shop.id")
    quantity: int = Field(ge=0)
    price: int = Field(ge=0)
    price_rrc: int = Field(ge=0)
    order_items: List["OrderItem"] = Relationship(back_populates="product_info")


class Parameter(SQLModel, table=True):

    __tablename__ = "parameter"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(max_length=40)
    product_parameters: List["ProductParameter"] = Relationship(back_populates="parameter")


class ProductParameter(SQLModel, table=True):

    __tablename__ = "product_parameter"

    id: Optional[int] = Field(primary_key=True)
    product_info_id: Optional[int] = Field(foreign_key="product_info.id")
    parameter_id: int = Field(foreign_key=Parameter.id)
    value: str = Field(max_length=100)


class Contact(SQLModel, table=True):

    __tablename__ = "contact"

    id: Optional[int] = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    city: str = Field(max_length=50)
    street: str = Field(max_length=100)
    house: Optional[str] = Field(max_length=15)
    structure: Optional[str] = Field(max_length=15)
    building: Optional[str] = Field(max_length=15)
    apartment: Optional[str] = Field(max_length=15)
    phone: str = Field(max_length=50)


class Order(SQLModel, table=True):

    __tablename__ = "order"

    id: Optional[int] = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    dt: datetime = Field(default_factory=TIMESTAMP)
    state: OrderEnum
    contact_id: Optional[int] = Field(foreign_key="contact.id")
    order_items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):

    __tablename__ = "order_item"

    id: Optional[int] = Field(primary_key=True)
    order_id: Optional[int] = Field(foreign_key="order.id")
    product_info_id: Optional[int] = Field(foreign_key="product_info.id")
    quantity: int = Field(ge=0)
