from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from . import models, schemas, utility
from .db import SessionLocal, engine
from .database.init_db import init_db, init_urls


#models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Primerjalnik cen")


@app.on_event("startup")
def on_startup():
    # models.Base.metadata.drop_all(bind=engine) ## just in case of errors
    # models.Base.metadata.create_all(bind=engine)
    db_tables = engine.table_names()
    if "products" not in db_tables:
        print(f"Creating product entries")
        init_db()
    if "urls" not in db_tables:
        print(f"Creating url entries")
        init_urls()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Add new product to the database
    """
    db_product = utility.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    return utility.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = utility.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = utility.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product and all its associated prices from the database
    """
    status = utility.delete_product(db, product_id=product_id)
    if status == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"Deleted":bool(status)}


@app.post("/products/{product_id}/prices/", response_model=schemas.Price)
def create_price_for_product(
    product_id: int, price: schemas.PriceCreate, db: Session = Depends(get_db)):
    return utility.create_product_price(db=db, price=price, product_id=product_id)


@app.get("/prices/", response_model=List[schemas.Price])
def read_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = utility.get_prices(db, skip=skip, limit=limit)
    return prices


@app.get("/products/name={product_name}/prices/", response_model=List[schemas.Price])
def read_prices_by_name(product_name: str, db: Session = Depends(get_db)):
    prices = utility.get_prices_by_name(db, name=product_name)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.get("/products/{product_id}/prices/", response_model=List[schemas.Price])
def read_prices_by_id(product_id: int, db: Session = Depends(get_db)):
    prices = utility.get_prices_by_id(db, id=product_id)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.get("/products/{product_id}/lowest_price/", response_model=schemas.Price)
def read_lowest_price(product_id: int, db: Session = Depends(get_db)):
    prices = utility.get_lowest_price(db, id=product_id)
    if prices is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return prices


@app.delete("/prices/{price_id}")
def delete_price(price_id: int, db: Session = Depends(get_db)):
    """
    Delete price with given id from the database
    """
    status = utility.delete_price(db, price_id)
    if status == 0:
        raise HTTPException(status_code=404, detail="Price entry not found")
    return {"Deleted":bool(status)}


@app.post("/prices/update/", response_model=List[schemas.Product])
def update_all_prices(db: Session = Depends(get_db)):
    products = utility.update_all_prices(db)
    return products


@app.get("/retailers/", response_model=List[str])
def get_retailers(db: Session = Depends(get_db)):
    retailers = utility.get_retailers(db)
    return retailers



# todo add link
