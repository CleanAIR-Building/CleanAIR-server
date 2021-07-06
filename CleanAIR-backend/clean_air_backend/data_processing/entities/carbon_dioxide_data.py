from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from .base import Base
import enum


class CarbonDioxideData(Base):
    __tablename__ = 'carbon_dioxide_data'

    class CO2LEVEL(enum.Enum):
        LOW = 0,
        HIGH = 1

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    sensor = Column(String)
    co2 = Column(Float)
    state = Column(Enum(CO2LEVEL))

    def __str__(self):
        return str(self.__dict__)
