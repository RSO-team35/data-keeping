from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

try:
    use_postgres = os.environ["DB_POSTGRES"]
    postgres_user = os.environ["DB_USER"]
    postgres_pass = os.environ["DB_PASS"]
    postgres_host = os.environ["DB_HOST"]
except:
    use_postgres = False

if use_postgres:
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{postgres_user}:{postgres_pass}@{postgres_host}/postgres'

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
else:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///sql_app/database/sql_app.db'

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
