#! bin/python3
from testcontainers.postgres import PostgresContainer
from data_processing.session import create_database_session
from data_processing.consumers.traffic_light_consumer import TrafficLightConsumer
from data_processing.entities.traffic_light_data import TrafficLightData
from test.utils.message import Message
from test.utils.system_state_mock import SystemStateMock
import unittest
import json


class test_TrafficLightData(unittest.TestCase):
    SENSOR_NAME = "traffic_light"
    RED = TrafficLightData.LIGHT.RED
    GREEN = TrafficLightData.LIGHT.GREEN
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
            results = session.query(TrafficLightData).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        TrafficLightData.__table__.drop(bind=self.engine)

    def test_GREEN(self):
        traffic_light_consumer: TrafficLightConsumer = TrafficLightConsumer("traffic_light", self.Session,
                                                                            self.system_state)
        msg = Message(topic="traffic_light", payload=json.dumps(
            {"state": test_TrafficLightData.GREEN.name, "sensor": test_TrafficLightData.SENSOR_NAME}))
        traffic_light_consumer.consume(test_TrafficLightData.PLACEHOLDER, test_TrafficLightData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(TrafficLightData).all()
            for result in results:
                self.assertEqual(test_TrafficLightData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_TrafficLightData.GREEN, result.state)

    def test_RED(self):
        traffic_light_consumer: TrafficLightConsumer = TrafficLightConsumer("traffic_light", self.Session,
                                                                            self.system_state)
        msg = Message(topic="traffic_light", payload=json.dumps(
            {"state": test_TrafficLightData.RED.name, "sensor": test_TrafficLightData.SENSOR_NAME}))
        traffic_light_consumer.consume(test_TrafficLightData.PLACEHOLDER, test_TrafficLightData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(TrafficLightData).all()
            for result in results:
                self.assertEqual(test_TrafficLightData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_TrafficLightData.RED, result.state)


if __name__ == "__main__":
    unittest.main()
