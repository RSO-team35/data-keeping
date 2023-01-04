from typing import List
from . import utility
from .utility import get_db
import strawberry
import datetime


@strawberry.type
class GQL_Price:
    id: int
    price: float
    date: datetime.datetime
    manufacturer: str
    retailer: str


@strawberry.type
class GQL_Product:
    id: int
    name: str
    category: str
    tags: str
    prices: List[GQL_Price]


def get_gql_product():
    db = next(get_db())
    products = utility.get_products(db)
    print(products[0].name)
    return [
        GQL_Product(
            id=product.id,
            name=product.name,
            category=product.category,
            tags=product.tags,
            prices=[GQL_Price(
                id=price.id,
                price=price.price,
                date=price.date,
                manufacturer=price.manufacturer,
                retailer=price.retailer
            )
            for price in product.prices]
        )
    for product in products]    


@strawberry.type
class Query:
    products: List[GQL_Product] = strawberry.field(resolver=get_gql_product)


schema = strawberry.Schema(Query)