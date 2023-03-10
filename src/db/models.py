from datetime import datetime
from enum import Enum
from typing import Optional, List, Literal

from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTypeEnum(str, Enum):
    BUYER = "buyer"
    SHOP = "shop"


class OrderStateEnum(str, Enum):
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
    username: str = Column(String(length=150), unique=True, nullable=False)
    usertype: Literal["buyer", "shop"] = Column(String(length=5), default="buyer")
    shop: "Shop" = relationship("Shop", back_populates="user")
    contacts: List["Contact"] = relationship("Contact", back_populates="user")
    orders: List["Order"] = relationship("Order", back_populates="user")

    __mapper_args__ = {"eager_defaults": True}


class ShopCategory(Base):

    __tablename__ = "shop_category"

    shop_id: int = Column(ForeignKey("shop.id", ondelete="cascade"), primary_key=True)
    category_id: int = Column(ForeignKey("category.id", ondelete="cascade"), primary_key=True)


class Shop(Base):

    __tablename__ = "shop"

    id: Optional[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=50), unique=True)
    url: str = Column(String)
    user_id: int = Column(Integer, ForeignKey("user.id", ondelete="cascade"))
    user: User = relationship("User", back_populates="shop")
    state: bool = Column(Boolean, default=True)
    products_info: List["ProductInfo"] = relationship("ProductInfo", back_populates="shop")
    categories: List["Category"] = relationship("Category",
                                                secondary="shop_category",
                                                back_populates="shops",
                                                # lazy="joined"
                                                )


class Category(Base):

    __tablename__ = "category"

    id: Optional[int] = Column(Integer, primary_key=True)
    name: str = Column(String(length=40), unique=True)
    shops: List[Shop] = relationship("Shop",
                                     secondary="shop_category",
                                     back_populates="categories",
                                     # lazy="joined"
                                     )
    products: List["Product"] = relationship("Product", back_populates="category")


class Product(Base):

    __tablename__ = "product"

    id: Optional[int] = Column(Integer, primary_key=True)
    name: str = Column(String(length=80))
    category_id: int = Column(Integer, ForeignKey("category.id", ondelete="cascade"))
    category: "Category" = relationship("Category", back_populates="products")
    products_info: List["ProductInfo"] = relationship("ProductInfo", back_populates="product")


class ProductInfo(Base):

    __tablename__ = "product_info"

    id: Optional[int] = Column(Integer, primary_key=True)
    model: str = Column(String(length=80))
    external_id: int = Column(Integer)
    product_id: int = Column(Integer, ForeignKey("product.id", ondelete="cascade"))
    product: Product = relationship("Product", back_populates="products_info")
    shop_id: int = Column(ForeignKey("shop.id"))
    shop: Shop = relationship("Shop", back_populates="products_info")
    quantity: int = Column(Integer)
    price: int = Column(Integer)
    price_rrc: int = Column(Integer)
    order_items: List["OrderItem"] = relationship("OrderItem", back_populates="product_info")
    product_parameters: List["ProductParameter"] = relationship("ProductParameter", back_populates="product_info")
    __table_args__ = (UniqueConstraint('product_id', 'shop_id', 'external_id', name='_unique_product_info'),
                      )
    

class Parameter(Base):

    __tablename__ = "parameter"

    id: Optional[int] = Column(Integer, primary_key=True)
    name: str = Column(String(length=40))
    product_parameters: List["ProductParameter"] = relationship("ProductParameter", back_populates="parameter")


class ProductParameter(Base):

    __tablename__ = "product_parameter"

    id: Optional[int] = Column(Integer, primary_key=True)
    product_info_id: int = Column(Integer, ForeignKey("product_info.id", ondelete="cascade"))
    product_info: ProductInfo = relationship("ProductInfo", back_populates="product_parameters")
    parameter_id: int = Column(Integer, ForeignKey("parameter.id", ondelete="cascade"))
    parameter: Parameter = relationship("Parameter", back_populates="product_parameters")
    value: str = Column(String(length=100))
    __table_args__ = (UniqueConstraint('product_info_id', 'parameter_id', name='_unique_product_info_parameter'),
                      )


class Contact(Base):

    __tablename__ = "contact"

    id: Optional[int] = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    user: User = relationship(User, back_populates="contacts")
    city: str = Column(String(length=50))
    street: str = Column(String(length=100))
    house: str = Column(String(length=15))
    structure: str = Column(String(length=15))
    building: str = Column(String(length=15))
    apartment: str = Column(String(length=15))
    phone: str = Column(String(length=50))


class Order(Base):

    __tablename__ = "order"

    id: Optional[int] = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id", ondelete="cascade"))
    user: User = relationship("User", back_populates="orders")
    dt_at: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    state: str = Column(String(length=10))
    contact_id: int = Column(Integer, ForeignKey("contact.id", ondelete="cascade"))
    order_items: List["OrderItem"] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):

    __tablename__ = "order_item"

    id: Optional[int] = Column(Integer, primary_key=True)
    order_id: int = Column(Integer, ForeignKey("order.id", ondelete="cascade"))
    order: Order = relationship("Order", back_populates="order_items")
    product_info_id: int = Column(Integer, ForeignKey("product_info.id", ondelete="cascade"))
    product_info: ProductInfo = relationship("ProductInfo", back_populates="order_items")
    quantity: int = Column(Integer)
    __table_args__ = (UniqueConstraint('order_id', 'product_info_id', name='unique_order_item'),
                      )
