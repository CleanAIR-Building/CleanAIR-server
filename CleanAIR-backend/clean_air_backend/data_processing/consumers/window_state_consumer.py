from sqlalchemy.orm import sessionmaker
from .consumer import Consumer
from ..entities.window_state_data import WindowStateData
from ..system_state import SystemState
import datetime
import logging


class WindowStateConsumer(Consumer):
    def __init__(self, topic: str, Session: sessionmaker, system_state: SystemState):
        Consumer.__init__(self, topic)
        self.system_state = system_state
        self.Session: sessionmaker = Session
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume(self, client, userdata, msg):
        payload = self.decodeAndLog(msg)
        now: datetime = datetime.datetime.now()
        sensor: str = payload["sensor"]
        if payload["window_state"] == "open" or payload["window_state"] == "closed":
            data = payload["window_state"]
            state: WindowStateData.WINDOW_STATE = WindowStateData.WINDOW_STATE.OPEN if data == "open" else WindowStateData.WINDOW_STATE.CLOSED
            self.logger.debug(f"Payload={data} | state={state}")
            with self.Session.begin() as session:
                entity = WindowStateData(time=now, sensor=sensor, state=state)
                session.add(entity)
                self.logger.info("Stored: {} ".format(entity))
            self.system_state.update_window_state(state)
        else:
            self.logger.info("Unknown state")
