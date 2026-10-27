import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
database_url = os.getenv("DATABASE_URL")
print(database_url)
engine = create_engine(
    database_url,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


def get_db():
    with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass


def create_table():
    Base.metadata.create_all(bind=engine)
