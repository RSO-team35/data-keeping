from sqlalchemy.orm import Session

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
