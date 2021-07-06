from sqlalchemy import Column, Integer, String, Enum, DateTime
from .base import Base
import enum


class InfraredData(Base):
    __tablename__ = 'infrared_data'

    class TEMPERATURE(enum.Enum):
        COLD = 0,
        HOT = 1

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    sensor = Column(String)
    state = Column(Enum(TEMPERATURE))

    def __str__(self):
        return str(self.__dict__)
