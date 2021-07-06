from mqtt.mqtt_client import MQTTClient
from orchestration.orchestration import Orchestrator
import unittest


class test_orchestration(unittest.TestCase):
    class MQTTClientMockBase(MQTTClient):
        def __init__(self, test_case):
            self.test_case = test_case

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

    def test_turn_light_on(self):
        class MQTTClientMock(test_orchestration.MQTTClientMockBase):
            def publish(self, topic: str, payload: dict):
                self.test_case.assertEqual("actuators/traffic-light", topic)
                self.test_case.assertEqual({"command": "RED"}, payload)

        orchestrator: Orchestrator = Orchestrator(MQTTClientMock(self))
        orchestrator.execute(["turn-light-on-dawai"])

    def test_turn_light_off(self):
        class MQTTClientMock(test_orchestration.MQTTClientMockBase):
            def publish(self, topic: str, payload: dict):
                self.test_case.assertEqual("actuators/traffic-light", topic)
                self.test_case.assertEqual({"command": "GREEN"}, payload)

        orchestrator: Orchestrator = Orchestrator(MQTTClientMock(self))
        orchestrator.execute(["turn-light-off-dawai"])

    def test_open_window(self):
        class MQTTClientMock(test_orchestration.MQTTClientMockBase):
            def publish(self, topic: str, payload: dict):
                self.test_case.assertEqual("actuators/window", topic)
                self.test_case.assertEqual({"command": "OPEN"}, payload)

        orchestrator: Orchestrator = Orchestrator(MQTTClientMock(self))
        orchestrator.execute(["open-window-dawai"])

    def test_close_window(self):
        class MQTTClientMock(test_orchestration.MQTTClientMockBase):
            def publish(self, topic: str, payload: dict):
                self.test_case.assertEqual("actuators/window", topic)
                self.test_case.assertEqual({"command": "CLOSE"}, payload)

        orchestrator: Orchestrator = Orchestrator(MQTTClientMock(self))
        orchestrator.execute(["close-window-dawai"])


if __name__ == "__main__":
    unittest.main()
