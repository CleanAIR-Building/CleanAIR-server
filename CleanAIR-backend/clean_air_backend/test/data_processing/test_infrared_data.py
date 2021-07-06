#! bin/python3
from testcontainers.postgres import PostgresContainer
from data_processing.consumers.infrared_consumer import InfraRedConsumer
from data_processing.session import create_database_session
from data_processing.entities.infrared_data import InfraredData
from test.utils.message import Message
from test.utils.system_state_mock import SystemStateMock
import unittest
import json


class test_InfraredData(unittest.TestCase):
    SENSOR_NAME = "infra"
    HOT = InfraredData.TEMPERATURE.HOT
    COLD = InfraredData.TEMPERATURE.COLD
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
            results = session.query(InfraredData).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        InfraredData.__table__.drop(bind=self.engine)

    def test_HOT(self):
        infra_red_consumer: InfraRedConsumer = InfraRedConsumer("infraRed", self.Session, self.system_state)
        msg = Message(topic="infraRed", payload=json.dumps(
            {"state": test_InfraredData.HOT.name, "sensor": test_InfraredData.SENSOR_NAME}))
        infra_red_consumer.consume(test_InfraredData.PLACEHOLDER, test_InfraredData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(InfraredData).all()
            for result in results:
                self.assertEqual(test_InfraredData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_InfraredData.HOT, result.state)

    def test_COLD(self):
        infra_red_consumer: InfraRedConsumer = InfraRedConsumer("infraRed", self.Session, self.system_state)
        msg = Message(topic="infraRed", payload=json.dumps(
            {"state": test_InfraredData.COLD.name, "sensor": test_InfraredData.SENSOR_NAME}))
        infra_red_consumer.consume(test_InfraredData.PLACEHOLDER, test_InfraredData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(InfraredData).all()
            for result in results:
                self.assertEqual(test_InfraredData.SENSOR_NAME, result.sensor)
                self.assertEqual(test_InfraredData.COLD, result.state)


if __name__ == "__main__":
    unittest.main()
