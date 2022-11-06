from typing import Union, List
from pydantic import BaseModel
import datetime


class PriceBase(BaseModel):
    price: int
    date: datetime.datetime
    retailer: str
    manufacturer: str


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    tags: str
    category: str
    

class ProductCreate(ProductBase):
    prices: Union[List[PriceBase], None] = None
    #price: Union[PriceBase, None] = None # when creating this will be unset
    #price: Union[float, None] = None this is when param is optional


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

