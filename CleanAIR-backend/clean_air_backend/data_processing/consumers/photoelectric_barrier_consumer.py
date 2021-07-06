from sqlalchemy.orm import sessionmaker
from .consumer import Consumer
from ..entities.photoelectric_data import PhotoElectricBarrierData
from ..system_state import SystemState
import datetime
import logging


class PhotoelectricBarrierConsumer(Consumer):
    def __init__(self, topic: str, Session: sessionmaker, system_state: SystemState, limit: int = 50):
        Consumer.__init__(self, topic)
        self.Session: sessionmaker = Session
        self.system_state = system_state
        self.count: int = 0
        self.logger = logging.getLogger(self.__class__.__name__)
        self.limit = limit

    def consume(self, client, userdata, msg):
        payload = self.decodeAndLog(msg)
        now: datetime = datetime.datetime.now()
        sensor: str = payload["sensor"]
        self.count += payload["count"]
        state = PhotoElectricBarrierData.OCCUPANCY_STATE.FULL if self.count >= self.limit else PhotoElectricBarrierData.OCCUPANCY_STATE.NOT_FULL
        with self.Session.begin() as session:
            entity = PhotoElectricBarrierData(time=now, sensor=sensor,state=state, count=self.count)
            session.add(entity)
            self.logger.info("Stored: {} ".format(entity))
        self.system_state.update_photo_electric_barrier_data(state)
