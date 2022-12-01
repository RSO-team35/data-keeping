from typing import Union, List
from pydantic import BaseModel, HttpUrl
import datetime


class PriceBase(BaseModel):
    price: float
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


class ProductSpec(BaseModel):
    retailer: str # could create custom type
    manufacturer: str
    model: str # Zotac Gaming etc
    name: str # Nvidia RTX 3060 Ti, this is a product name
    url: HttpUrl

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "retailer": "Mimovrste",
                "manufacturer": "ASUS",
                "model": "ASUS ROG Strix",
                "name": "NVIDIA RTX 3090",
                "url": "https://www.mimovrste.com/graficne-kartice-nvidia/asus-rog-strix-gaming-oc-geforce-rtx-3090-graficna-kartica-24-gb-gddr6x",
            }
        }