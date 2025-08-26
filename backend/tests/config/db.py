from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config import database_name
from src.db.connection import BaseModel
from src import config, secrets
import pytest
from contextlib import contextmanager
from src import db

def test_database_name():
    return database_name() + "_test"


@pytest.fixture(scope="session")
def create_test_database():
    engine = create_engine(
        "postgresql+psycopg://{user}:{password}@{host}:{port}".format(
            user=secrets.database_user(),
            host=config.database_host(),
            port=config.database_port(),
            password=secrets.database_password(),
        ),
        isolation_level="AUTOCOMMIT",
    )
    
    with engine.connect() as connection:
        connection.execute(text("DROP DATABASE IF EXISTS {db_name}".format(db_name=test_database_name()))) 
        connection.execute(text("CREATE DATABASE {db_name}".format(db_name=test_database_name()))) 
    engine.dispose()



@pytest.fixture(scope="session")
def database_engine(create_test_database):
    return create_engine(
        "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}".format(
            user="postgres",
            password="postgres",
            host=config.database_host(),
            port=config.database_port(),
            database=test_database_name()
        )
    )



@pytest.fixture(scope="session")
def connection(database_engine):
    with database_engine.connect() as connection:
        with connection.begin():
            BaseModel.metadata.create_all(connection)
            connection.execute(text("CREATE EXTENSION pg_trgm;"))
    
        yield connection
        
    connection.close()
    
    
@pytest.fixture
def db_session(connection, monkeypatch):
    transactoin = connection.begin()
    session_factory = sessionmaker(bind=connection)
    
    @contextmanager
    def session_factory_context_manager():
        connection.begin_nested()
        yield session_factory()
        
    monkeypatch.setattr(
        db.connection,
        "_session",
        session_factory_context_manager
    )
    
    session = session_factory()
    yield session
    transactoin.rollback()