from sqlalchemy import Column, Integer, String, Enum, DateTime
from .base import Base
import enum


class WindowStateData(Base):
    __tablename__ = 'window_state_data'

    class WINDOW_STATE(enum.Enum):
        CLOSED = 0,
        OPEN = 1

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    sensor = Column(String)
    state = Column(Enum(WINDOW_STATE))

    def __str__(self):
        return str(self.__dict__)
