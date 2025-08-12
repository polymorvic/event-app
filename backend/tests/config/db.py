from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from src.config import database_name
from typing import Generator

from src import config, secrets
import pytest


def test_database_name():
    return database_name() + "_test"


@pytest.fixture()
def get_test_database():
    engine = create_engine(
        "postgresql+psycopg://{user}:{password}@{host}:{port}/{database_name}".format(
            host=config.database_host(),
            port=config.database_port(),
            database_name=test_database_name,
            user=secrets.database_user(),
            password=secrets.database_password(),
        )
    )
    
    with engine.connect() as connection:
        connection.execute(text("DROP DATABASE IF EXISTS {db_name}".format(db_name=test_database_name))) 
        connection.execute(text("CREATE DATABASE {db_name}".format(db_name=test_database_name))) 
    engine.dispose()
