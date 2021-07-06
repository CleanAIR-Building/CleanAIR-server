from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from .entities import Base


def create_database_session(url: str):
    engine = create_engine(url, future=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        engine.connect()
    Session = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(engine, checkfirst=True)
    return Session, engine
