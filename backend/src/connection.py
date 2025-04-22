from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


from src import config


def database_url() -> str:
    return "postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        host="a",
        port="q",
        database="a",
        user="asd",
        password="asd"
    )