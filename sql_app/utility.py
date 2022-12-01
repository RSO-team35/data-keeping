from sqlalchemy.orm import Session
import requests
import os
from . import models, schemas


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(db: Session, product_id: int):
    status = db.query(models.Product).filter(models.Product.id == product_id).delete()
    db.query(models.Price).filter(models.Price.product_id == product_id).delete()
    db.commit()
    return status


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, tags=product.tags, category=product.category, prices=[])
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


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


def update_all_prices(db: Session):
    # get urls
    db_urls = db.query(models.Urls).all()
    # request prices from data acquisition app
    data_keeping_ip = "http://127.0.0.1:8008/prices/" #os.environ["DATA_KEEPING_PORT"] # locally must change later
    response = requests.post(data_keeping_ip, json=db_urls)
    print(response.status_code)
    # update prices in database
    new_prices = response.content
    for price, url in zip(new_prices, db_urls):
        product = get_product_by_name(db, url.name)
        create_product_price(db, price=price, product_id=product.id)
    # fin
    return get_products(db)