import datetime
import json
from sql_app import models
from sql_app.db import SessionLocal, engine


def init_db():
    db = SessionLocal()
    ## add delete when exists stuff, drop all or sth

    models.Base.metadata.create_all(bind=engine)

    products = ["3050", "3060", "3060 Ti", "3070", "3070 Ti", "3080", "3080 Ti", "3090", "3090 Ti", "4090"]

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


def create_db():
    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    with open("sql_app/database/export_products.json", "r") as f:
        products_data = json.load(f)[0]
        header = products_data["header"]
        products = products_data["rows"]

    #print(products)

    for row in products:
        db_product = models.Product(id=int(row[0]), 
                                    name=row[1],
                                    category=row[2],
                                    tags=row[3],
                                    prices=[])

        db.add(db_product)
    db.commit()
    db.close()

    with open("sql_app/database/export_prices.json", "r") as f:
        prices_data = json.load(f)[0]
        header = prices_data["header"]
        prices = prices_data["rows"]

    #print(prices)

    for row in prices:
        db_price = models.Price(id=int(row[0]), 
                                    price=float(row[1]),
                                    date=datetime.datetime.fromisoformat(row[2]),
                                    retailer=row[3],
                                    manufacturer=row[4],
                                    product_id=int(row[5]))
        db.add(db_price)
    db.commit()
    db.close()

    

def init_urls():
    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    with open("sql_app/database/urls.json", "r") as f:
        prices_data = json.load(f)

    for retailer in prices_data:
        for name in prices_data[retailer]:
            for model in prices_data[retailer][name]:
                mf = model.split(" ")[0]
                md = " ".join(model.split(" ")[1:])
                db_url = models.Url(name=name,
                                        retailer=retailer,
                                        model=md,
                                        manufacturer=mf,
                                        url=prices_data[retailer][name][model])
                db.add(db_url)
    
    db.commit()
