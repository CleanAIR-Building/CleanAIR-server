from sqlalchemy import Column, Integer, String, DateTime, Enum
from .base import Base
import enum


class PhotoElectricBarrierData(Base):
    __tablename__ = 'photo_electric_data'

    class OCCUPANCY_STATE(enum.Enum):
        NOT_FULL = 0,
        FULL = 1

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    sensor = Column(String)
    state = Column(Enum(OCCUPANCY_STATE))
    count = Column(Integer)

    def __str__(self):
        return str(self.__dict__)
