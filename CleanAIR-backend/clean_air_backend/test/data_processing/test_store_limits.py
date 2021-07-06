from testcontainers.postgres import PostgresContainer
from data_processing.entities.limit import Limit, store_limits
from data_processing.session import create_database_session
import unittest


class test_store_limits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres = PostgresContainer("postgres:9.5")
        cls.postgres.start()

    @classmethod
    def tearDownClass(cls):
        cls.postgres.stop()

    def setUp(self):
        self.Session, self.engine = create_database_session(self.postgres.get_connection_url())
        with self.Session.begin() as session:
            results = session.query(Limit).all()
            self.assertEqual(0, len(results))

    def tearDown(self):
        Limit.__table__.drop(bind=self.engine)

    def test_storage(self):
        expected = [Limit(name="co2_limit", limit=500), Limit(name="occupation_limit", limit=50)]
        store_limits(self.Session, expected[0].limit, expected[1].limit)
        with self.Session.begin() as session:
            actual = session.query(Limit).order_by(Limit.limit.desc()).all()
            self.assertEqual(expected, actual)

    def test_overwrite(self):
        expected = [Limit(name="co2_limit", limit=500), Limit(name="occupation_limit", limit=50)]
        store_limits(self.Session, expected[0].limit, expected[1].limit)
        with self.Session.begin() as session:
            actual = session.query(Limit).order_by(Limit.limit.desc()).all()
            self.assertEqual(expected, actual)

        expected = [Limit(name="co2_limit", limit=999999999999), Limit(name="occupation_limit", limit=0.1)]
        store_limits(self.Session, expected[0].limit, expected[1].limit)
        with self.Session.begin() as session:
            actual = session.query(Limit).order_by(Limit.limit.desc()).all()
            self.assertEqual(expected, actual)
