#! bin/python3
from testcontainers.postgres import PostgresContainer
from data_processing.consumers.photoelectric_barrier_consumer import PhotoelectricBarrierConsumer
from data_processing.session import create_database_session
from data_processing.entities.photoelectric_data import PhotoElectricBarrierData
from test.utils.message import Message
from test.utils.system_state_mock import SystemStateMock
import unittest
import json


class test_PhotoElectricBarrierData(unittest.TestCase):
    SENSOR_NAME = "photo_electric"
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
            results = session.query(PhotoElectricBarrierData).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        PhotoElectricBarrierData.__table__.drop(bind=self.engine)

    def test_NOT_FULL(self):
        photoelectricBarrierConsumer: PhotoelectricBarrierConsumer = PhotoelectricBarrierConsumer("photo_electric",
                                                                                                  self.Session,
                                                                                                  self.system_state)
        msg = Message(topic="photo_electric",
                      payload=json.dumps({"count": 49, "sensor": test_PhotoElectricBarrierData.SENSOR_NAME}))
        photoelectricBarrierConsumer.consume(test_PhotoElectricBarrierData.PLACEHOLDER,
                                             test_PhotoElectricBarrierData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(PhotoElectricBarrierData).all()
            for result in results:
                self.assertEqual(test_PhotoElectricBarrierData.SENSOR_NAME, result.sensor)
                self.assertEqual(49, result.count)
                self.assertEqual(PhotoElectricBarrierData.OCCUPANCY_STATE.NOT_FULL, result.state)

    def test_FULL(self):
        photoelectricBarrierConsumer: PhotoelectricBarrierConsumer = PhotoelectricBarrierConsumer("photo_electric",
                                                                                                  self.Session,
                                                                                                  self.system_state)
        msg = Message(topic="photo_electric",
                      payload=json.dumps({"count": 9999, "sensor": test_PhotoElectricBarrierData.SENSOR_NAME}))
        photoelectricBarrierConsumer.consume(test_PhotoElectricBarrierData.PLACEHOLDER,
                                             test_PhotoElectricBarrierData.PLACEHOLDER, msg)
        with self.Session.begin() as session:
            results = session.query(PhotoElectricBarrierData).all()
            for result in results:
                self.assertEqual(test_PhotoElectricBarrierData.SENSOR_NAME, result.sensor)
                self.assertEqual(9999, result.count)
                self.assertEqual(PhotoElectricBarrierData.OCCUPANCY_STATE.FULL, result.state)


if __name__ == "__main__":
    unittest.main()
