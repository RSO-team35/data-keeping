import datetime

from sql_app import models
from sql_app.db import SessionLocal, engine


def init_db():
    db = SessionLocal()
    ## add delete when exists stuff, drop all or sth

    models.Base.metadata.create_all(bind=engine)

    products = ["3050", "3060", "3070"]

    for p in products:
        db_product = models.Product(name=f"GeForce RTX {p}", 
                                    tags=f"GeForce,RTX,{p}", 
                                    category="GPU", 
                                    prices=[])
        db.add(db_product)
    db.commit()

    prices = [350, 400, 299, 600, 560]

    for i, p in enumerate(prices):
        db_price = models.Price(price=p, 
                                date=datetime.datetime(2022, 10, i+1), 
                                retailer="Amazon", 
                                manufacturer="ASUS", 
                                product_id=i%3+1)
        db.add(db_price)

    db.commit()
    db.close()