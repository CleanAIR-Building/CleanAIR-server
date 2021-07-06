from sqlalchemy import Column, Integer, String, Enum, DateTime
from .base import Base
import enum


class TrafficLightData(Base):
    __tablename__ = 'traffic_light_data'

    class LIGHT(enum.Enum):
        RED = 0,
        GREEN = 1

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    sensor = Column(String)
    state = Column(Enum(LIGHT))

    def __str__(self):
        return str(self.__dict__)
