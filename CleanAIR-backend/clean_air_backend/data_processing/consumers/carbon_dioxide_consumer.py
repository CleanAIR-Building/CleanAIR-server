from sqlalchemy.orm import sessionmaker
from .consumer import Consumer
from ..entities.carbon_dioxide_data import CarbonDioxideData
from data_processing.system_state import SystemState
import datetime
import logging


class CarbonDioxideConsumer(Consumer):
    def __init__(self, topic: str, Session: sessionmaker, system_state: SystemState, limit: float = 500.0):
        Consumer.__init__(self, topic)
        self.Session: sessionmaker = Session
        self.system_state = system_state
        self.limit = limit
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume(self, client, userdata, msg):
        payload = self.decodeAndLog(msg)
        now: datetime = datetime.datetime.now()
        sensor: str = payload["sensor"]
        state: CarbonDioxideData.CO2LEVEL = CarbonDioxideData.CO2LEVEL.HIGH if float(
            payload["eCO2"]) > self.limit else CarbonDioxideData.CO2LEVEL.LOW
        with self.Session.begin() as session:
            entity = CarbonDioxideData(time=now, sensor=sensor, state=state, co2=payload["eCO2"])
            session.add(entity)
            self.logger.info("Stored: {} ".format(entity))
        self.system_state.update_carbon_dioxide_amount(state)
