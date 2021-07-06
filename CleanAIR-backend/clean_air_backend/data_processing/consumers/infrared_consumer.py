from sqlalchemy.orm import sessionmaker
from .consumer import Consumer
from ..entities.infrared_data import InfraredData
from ..system_state import SystemState
import datetime
import logging


class InfraRedConsumer(Consumer):
    def __init__(self, topic: str, Session: sessionmaker, system_state: SystemState):
        Consumer.__init__(self, topic)
        self.system_state = system_state
        self.Session: sessionmaker = Session
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume(self, client, userdata, msg):
        payload = self.decodeAndLog(msg)
        now: datetime = datetime.datetime.now()
        sensor: str = payload["sensor"]
        if payload["state"] == "State.HOT" or payload["state"] == "State.COLD":
            state: InfraredData.TEMPERATURE = InfraredData.TEMPERATURE.HOT if payload["state"] == "State.HOT" else InfraredData.TEMPERATURE.COLD
            with self.Session.begin() as session:
                entity=InfraredData(time=now, sensor=sensor, state=state)
                session.add(entity)
                self.logger.info("Stored: {} ".format(entity))
            self.system_state.update_infrared_data(state)
        else:
            self.logger.info("Unknown state")
