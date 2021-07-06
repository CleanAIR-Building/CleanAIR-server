from config.config import config
import os
import unittest


class test_orchestration(unittest.TestCase):
    FILE = os.path.join(os.path.dirname(__file__), "resources/clean_air_backend_test.ini")

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_ini(self):
        expected: dict = {"host": "localhost", "client_name": "data_processing12", "user": "user1", "password": "user1"}
        actual: dict = config(section="mqtt", filename=test_orchestration.FILE)
        self.assertEqual(expected, actual)

        expected: dict = {"topic": "sensors/photoElectric", "limit": "50"}
        actual: dict = config(section="occupancy", filename=test_orchestration.FILE)
        self.assertEqual(expected, actual)

    def test_config_doesnt_exist(self):
        with self.assertRaises(FileNotFoundError):
            config(section="Not important", filename="./I/dont/exist.ini")

    def test_key_doesnt_exist(self):
        with self.assertRaises(KeyError):
            config(section="I don't exist", filename=test_orchestration.FILE)

        if __name__ == "__main__":
            unittest.main()
