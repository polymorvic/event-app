from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from typing import Generator

from src import config, secrets


def database_url() -> str:
    return (
        "postgresql+psycopg://{user}:{password}@{host}:{port}/{database_name}".format(
            host=config.database_host(),
            port=config.database_port(),
            database_name=config.database_name(),
            user=secrets.database_user(),
            password=secrets.database_password(),
        )
    )


engine = create_engine(database_url())

_session = sessionmaker(bind=engine)


class BaseModel(DeclarativeBase):
    def ___repr__(self) -> str:
        return str(self)


def db_session() -> Generator[Session, None, None]:
    with _session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
