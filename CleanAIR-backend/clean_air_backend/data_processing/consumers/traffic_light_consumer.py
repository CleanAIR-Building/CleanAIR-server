from sqlalchemy.orm import sessionmaker
from .consumer import Consumer
from ..entities.traffic_light_data import TrafficLightData
from ..system_state import SystemState
import datetime
import logging


class TrafficLightConsumer(Consumer):
    def __init__(self, topic: str, Session: sessionmaker, system_state: SystemState):
        Consumer.__init__(self, topic)
        self.system_state = system_state
        self.Session: sessionmaker = Session
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume(self, client, userdata, msg):
        payload = self.decodeAndLog(msg)
        now: datetime = datetime.datetime.now()
        sensor: str = payload["sensor"]
        if payload["state"] == "RED" or payload["state"] == "GREEN":
            state: TrafficLightData.LIGHT = TrafficLightData.LIGHT.RED if payload["state"] == "RED" else TrafficLightData.LIGHT.GREEN
            with self.Session.begin() as session:
                entity = TrafficLightData(time=now, sensor=sensor, state=state)
                session.add(entity)
                self.logger.info("Stored: {} ".format(entity))
            self.system_state.update_traffic_light_state(state)
        else:
            self.logger.info("Unknown state")
