from abc import ABC, abstractmethod
from mqtt.mqtt_client import MQTTClient


class Operator(ABC):
    def __init__(self, mqtt_client: MQTTClient):
        self.mqtt_client = mqtt_client

    @abstractmethod
    def execute(self):
        pass
