from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    func,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    company: str = Column(String(length=40), nullable=False)
    position
    username
    usertype
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


shop_category = Table(
    "shop_category",
    Base.metadata,
    Column("shop_id", ForeignKey("shops.id", ondelete="CASCADE")),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"))
)


class Shop(Base):

    __tablename__ = "shops"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String, nullable=False)
    state = Column(Boolean, default=True, nullable=False)
    products = relationship("ProductInfo", back_populates="products")


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    shops = relationship(Shop, secondary="shop_category", back_populates="shops")
    products = relationship("Product", back_populates="products")


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    category_id = Column(Integer,
                         ForeignKey("categories.id", ondelete="CASCADE"),
                         nullable=False)


class ProductInfo(Base):

    __tablename__ = "product_info"

    id = Column(Integer, primary_key=True)
    model = Column(String(80))
    external_id = Column(Integer, nullable=False),
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"))
    quantity = Column(Integer)
    price = Column(Integer)
    price_rrc = Column(Integer)
    ordered_items = relationship("OrderItem", back_populates="product_info")


class Parameter(Base):

    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)


class ProductParameter(Base):

    __tablename__ = "product_parameter"

    id = Column(Integer, primary_key=True)
    product_info = Column(Integer,
                          ForeignKey("product_info.id", ondelete="CASCADE"),
                          nullable=False),
    parameter_id = Column(Integer,
                          ForeignKey("parameters.id", ondelete="CASCADE"),
                          nullable=False)
    value = Column(String(100))


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    # user_id =
    city = Column(String(50))
    street = Column(String(100))
    house = Column(String(15))
    structure = Column(String(15))
    building = Column(String(15))
    apartment = Column(String(15))
    phone = Column(String(50))


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    # user_id =
    dt = Column(DateTime, server_default=func.utcnow)
    state = Column(String(15))  # choices=STATE_CHOICES
    contact_id = Column(Integer,
                        ForeignKey("contacts.id", ondelete="CASCADE"))
    ordered_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer,
                      ForeignKey("orders.id", ondelete="CASCADE"),
                      nullable=False)
    order = relationship("orders", back_populates="ordered_items")
    product_info_id = Column(Integer,
                             ForeignKey("product_info.id", ondelete="CASCADE"),
                             nullable=False)
    product_info = relationship("product_info", back_populates="ordered_items")
    quantity = Column(Integer)
