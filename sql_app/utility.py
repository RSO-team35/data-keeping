from sqlalchemy.orm import Session
from sqlalchemy import func
import httpx
import os
import time
import datetime
from . import models, schemas

from .db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    status = db.query(models.Product).filter(models.Product.id == product_id).delete()
    db.query(models.Price).filter(models.Price.product_id == product_id).delete()
    db.commit()
    return status


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_products(db: Session):
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, tags=product.tags, category=product.category, prices=[])
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_prices(db: Session):
    return db.query(models.Price).all()


def create_product_price(db: Session, price: schemas.PriceCreate, product_id: int):
    db_price = models.Price(**price.dict(), product_id=product_id)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def delete_price(db: Session, price_id: int):
    status = db.query(models.Price).filter(models.Price.id == price_id).delete()
    db.commit()
    return status


async def update_all_prices(db: Session):
    # get urls
    #db_urls = db.query(models.Url).all()
    #db_urls_dict = [dict(schemas.Url.from_orm(d)) for d in db_urls]
    # print(type(db_urls[0]))
    # print(dict(db_urls[0]))
    # request prices from data acquisition app
    try: 
        data_acq_ip = os.environ["DATA_ACQUISITION_IP"]
    except:
        data_acq_ip = "0.0.0.0:8001"# # locally must change later

    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }
    print("requesting prices...")
    t1 = time.time()
    #response = requests.post(f"http://{data_acq_ip}/prices/", json=db_urls_dict, headers=headers)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{data_acq_ip}/prices/", headers=headers, timeout=300)
    t2 = time.time()
    print(f"Status: {response.status_code}, duration: {t2-t1}s")
    # print(response)
    # update prices in database
    new_prices = response.json()
    print("saving new prices...")
    # print(new_prices)
    for price in new_prices:
        #print(price)
        price["date"] = datetime.datetime.fromisoformat(price["date"])
        #print(price["date"])
        product = get_product_by_name(db, price["name"])
        #model=item.model, name=item.name, price=item_price.price, date=item_price.date, retailer=item_price.retailer, manufacturer=item_price.manufacturer
        # db_price = models.Price(price=price["price"], retailer=price["retailer"], manufacturer=price["manufacturer"], date=price["date"], product_id=product.id)
        # db.add(db_price)
        # db.commit()
        # db.refresh(db_price)
        db_price = schemas.PriceCreate(price=price["price"], date=price["date"], retailer=price["retailer"], manufacturer=price["manufacturer"])
        create_product_price(db, price=db_price, product_id=product.id)
    # fin
    print("new prices saved")
    return #get_products(db)


def get_urls(db: Session):
    db_urls = db.query(models.Url).all()
    return db_urls

def get_retailers(db: Session):
    db_retailers = db.query(models.Url.retailer).distinct().all()
    db_retailers = [r[0] for r in db_retailers]
    return db_retailers


def get_prices_by_name(db: Session, name: str):
    product = get_product_by_name(db, name)
    if not product:
        return None
    db_prices = get_prices_by_id(db, product.id)
    return db_prices


def get_prices_by_id(db: Session, id: int):
    status = db.query(models.Product).filter(models.Product.id == id).first()
    if status is None:
        return None
    db_prices = db.query(models.Price).filter(models.Price.product_id == id).order_by(models.Price.price.desc()).all()
    return db_prices


def get_lowest_price(db: Session, id: int):
    status = db.query(models.Product).filter(models.Product.id == id).first()
    if status is None:
        return None
    db_price = db.query(models.Price).filter(models.Price.product_id == id, models.Price.price > 0).order_by(models.Price.price.asc()).first()
    return db_price
