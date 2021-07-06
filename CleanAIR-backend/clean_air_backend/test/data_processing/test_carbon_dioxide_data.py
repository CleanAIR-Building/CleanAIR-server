#! bin/python3
from testcontainers.postgres import PostgresContainer
from data_processing.consumers.carbon_dioxide_consumer import CarbonDioxideConsumer
from data_processing.session import create_database_session
from data_processing.entities.carbon_dioxide_data import CarbonDioxideData
from test.utils.message import Message
from test.utils.system_state_mock import SystemStateMock
import unittest
import json


class test_CarbonDioxideData(unittest.TestCase):
    SENSOR_NAME = "carbonDioxide"
    HIGH = 700
    LOW = 200
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
            results = session.query(CarbonDioxideData).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        CarbonDioxideData.__table__.drop(bind=self.engine)

    def test_HIGH(self):
        carbon_dioxide_consumer: CarbonDioxideConsumer = CarbonDioxideConsumer("infraRed", self.Session,
                                                                               self.system_state, 500.0)
        msg = Message(topic="carbonDioxide", payload=json.dumps(
            {"eCO2": test_CarbonDioxideData.HIGH, "sensor": test_CarbonDioxideData.SENSOR_NAME}))
        carbon_dioxide_consumer.consume(test_CarbonDioxideData.PLACEHOLDER, test_CarbonDioxideData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(CarbonDioxideData).all()
            for result in results:
                self.assertEqual(test_CarbonDioxideData.SENSOR_NAME, result.sensor)
                self.assertEqual(CarbonDioxideData.CO2LEVEL.HIGH, result.state)
                self.assertEqual(test_CarbonDioxideData.HIGH, result.co2)

    def test_LOW(self):
        carbon_dioxide_consumer: CarbonDioxideConsumer = CarbonDioxideConsumer("infraRed", self.Session,
                                                                               self.system_state, 500.0)
        msg = Message(topic="infraRed", payload=json.dumps(
            {"eCO2": test_CarbonDioxideData.LOW, "sensor": test_CarbonDioxideData.SENSOR_NAME}))
        carbon_dioxide_consumer.consume(test_CarbonDioxideData.PLACEHOLDER, test_CarbonDioxideData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(CarbonDioxideData).all()
            for result in results:
                self.assertEqual(test_CarbonDioxideData.SENSOR_NAME, result.sensor)
                self.assertEqual(CarbonDioxideData.CO2LEVEL.LOW, result.state)
                self.assertEqual(test_CarbonDioxideData.LOW, result.co2)


if __name__ == "__main__":
    unittest.main()
