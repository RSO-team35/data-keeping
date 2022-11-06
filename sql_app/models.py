from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY, DateTime, Float
from sqlalchemy.orm import relationship

from .db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)
    tags = Column(String)

    prices = relationship("Price", back_populates="product")


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, index=True)
    date = Column(DateTime, index=True)
    retailer = Column(String)
    manufacurer = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="prices")
