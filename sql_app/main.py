from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, utility, graphql
from .utility import get_db
from .db import SessionLocal, engine, use_postgres
from .database.init_db import init_db, init_urls, create_db

from strawberry.fastapi import GraphQLRouter

description = "Service for data keeping and organization"
tags_metadata = [
    {
        "name": "products",
        "description": "Operations with GPU products"
    },
    {
        "name": "prices",
        "description": "Operations with price data"
    }
]

graphql_app = GraphQLRouter(graphql.schema,graphiql=True)

app = FastAPI(title="Price comparison", description=description, openapi_tags=tags_metadata, docs_url="/openapi")

#maybe remove if api calls wont be done directly from frontend?
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql",tags=["products"])

@app.on_event("startup")
def on_startup():
    """
    Initialize database if it does not exist
    """
    db_tables = engine.table_names()

    if "products" not in db_tables:
        print(f"Creating product entries")
        create_db()

    if "urls" not in db_tables:
        print(f"Creating url entries")
        init_urls()


@app.post("/products/", response_model=schemas.Product, tags=["products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Add new product to the database
    """
    db_product = utility.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    return utility.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product], tags=["products"])
def read_products(db: Session = Depends(get_db)):
    """
    Get list of all products
    """
    products = utility.get_products(db)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get product with <product_id>
    """
    db_product = utility.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product and all its associated prices from the database
    """
    status = utility.delete_product(db, product_id=product_id)
    if status == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"Deleted":bool(status)}


@app.post("/products/{product_id}/prices/", response_model=schemas.Price, tags=["products"])
def create_price_for_product(product_id: int, price: schemas.PriceCreate, db: Session = Depends(get_db)):
    """
    Create new price entry for a product with <product_id>
    """
    return utility.create_product_price(db=db, price=price, product_id=product_id)


@app.get("/prices/", response_model=List[schemas.Price], tags=["prices"])
def read_prices(db: Session = Depends(get_db)):
    """
    Get all saved prices
    """
    prices = utility.get_prices(db)
    return prices


@app.get("/products/name={product_name}/prices/", response_model=List[schemas.Price], tags=["products"])
def read_prices_by_name(product_name: str, db: Session = Depends(get_db)):
    """
    Get all prices for a product with <name>
    """
    prices = utility.get_prices_by_name(db, name=product_name)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.get("/products/{product_id}/prices/", response_model=List[schemas.Price], tags=["products"])
def read_prices_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Get all prices for a product with <product_id>
    """
    prices = utility.get_prices_by_id(db, id=product_id)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.get("/products/{product_id}/lowest_price/", response_model=schemas.Price, tags=["products"])
def read_lowest_price(product_id: int, db: Session = Depends(get_db)):
    """
    Get lowest price for a product with <product_id>
    """
    prices = utility.get_lowest_price(db, id=product_id)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.delete("/prices/{price_id}", tags=["prices"])
def delete_price(price_id: int, db: Session = Depends(get_db)):
    """
    Delete price with given id from the database
    """
    status = utility.delete_price(db, price_id)
    if status == 0:
        raise HTTPException(status_code=404, detail="Price entry not found")
    return {"Deleted":bool(status)}


@app.post("/prices/update/", tags=["prices"])
async def update_all_prices(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Create new prices entry for all products from live data
    """
    background_tasks.add_task(utility.update_all_prices, db)
    #products = await utility.update_all_prices(db)
    return {"message": "Updating prices in the background"}


@app.get("/retailers/", response_model=List[str], tags=["products"])
def get_retailers(db: Session = Depends(get_db)):
    """
    Get all retailers available
    """
    retailers = utility.get_retailers(db)
    return retailers


@app.get("/products/urls/", response_model=List[schemas.Url], tags=["products"])
def get_urls(db: Session = Depends(get_db)):
    """
    Get all saved urls for price acquisition
    """
    urls = utility.get_urls(db)
    return urls


@app.get("/test/", tags=["products"])
def get_test(db: Session = Depends(get_db)):
    """
    Get all saved urls for price acquisition
    """
    create_db_pg()
    return "hehe"
