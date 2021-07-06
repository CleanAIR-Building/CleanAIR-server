from .base import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)


class Limit(Base):
    __tablename__ = "limit"

    name = Column(String, primary_key=True)
    limit = Column(Float)

    def __eq__(self, other):
        if isinstance(other, Limit):
            return self.name == other.name and self.limit == other.limit
        return False

    def __str__(self):
        return str(self.__dict__)


def store_limits(Session: sessionmaker, co2_limit: float, occupation_limit: float):
    co2_limit_entity = Limit(name="co2_limit", limit=co2_limit)
    occupation_limit_entity = Limit(name="occupation_limit", limit=occupation_limit)
    with Session.begin() as session:
        session.query(Limit).delete()
        session.add_all([co2_limit_entity, occupation_limit_entity])
        logger.info(
            "Stored limits: {co2_limit_entity} and {occupation_limit_entity}".format(co2_limit_entity=co2_limit_entity,
                                                                                     occupation_limit_entity=occupation_limit_entity))
