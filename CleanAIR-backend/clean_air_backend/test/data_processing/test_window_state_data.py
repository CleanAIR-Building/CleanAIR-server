#! bin/python3
from testcontainers.postgres import PostgresContainer
from data_processing.session import create_database_session
from data_processing.consumers.window_state_consumer import WindowStateConsumer
from data_processing.entities.window_state_data import WindowStateData
from test.utils.message import Message
from test.utils.system_state_mock import SystemStateMock
import unittest
import json


class test_WindowStateData(unittest.TestCase):
    SENSOR_NAME = "window"
    CLOSED = WindowStateData.WINDOW_STATE.CLOSED
    OPEN = WindowStateData.WINDOW_STATE.OPEN
    PLACEHOLDER = {}

    @classmethod
    def setUpClass(cls):
        cls.postgres = PostgresContainer("postgres:9.5")
        cls.postgres.start()
        cls.system_state = SystemStateMock()

    @classmethod
    def tearDownClass(cls):
        cls.postgres.stop()

    def setUp(self):
        self.Session, self.engine = create_database_session(self.postgres.get_connection_url())
        with self.Session.begin() as session:
            results = session.query(WindowStateData).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        WindowStateData.__table__.drop(bind=self.engine)

    def test_CLOSED(self):
        windowStateConsumer: WindowStateConsumer = WindowStateConsumer("window", self.Session, self.system_state)
        msg = Message(topic="window", payload=json.dumps(
            {"window_state": test_WindowStateData.CLOSED.name, "sensor": test_WindowStateData.SENSOR_NAME}))
        windowStateConsumer.consume(test_WindowStateData.PLACEHOLDER, test_WindowStateData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(WindowStateData).all()
            for result in results:
                self.assertEqual(test_WindowStateData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_WindowStateData.CLOSED, result.state)

    def test_OPEN(self):
        windowStateConsumer: WindowStateConsumer = WindowStateConsumer("window", self.Session, self.system_state)
        msg = Message(topic="window", payload=json.dumps(
            {"window_state": test_WindowStateData.OPEN.name, "sensor": test_WindowStateData.SENSOR_NAME}))
        windowStateConsumer.consume(test_WindowStateData.PLACEHOLDER, test_WindowStateData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(WindowStateData).all()
            for result in results:
                self.assertEqual(test_WindowStateData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_WindowStateData.OPEN, result.state)


if __name__ == "__main__":
    unittest.main()
