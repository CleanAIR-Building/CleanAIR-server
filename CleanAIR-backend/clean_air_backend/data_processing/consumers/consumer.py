from abc import ABC, abstractmethod
import logging
import json


class Consumer(ABC):
    @abstractmethod
    def __init__(self, topic: str):
        self.topic = topic
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def consume(self, client, userdata, msg):
        pass

    def decodeAndLog(self, msg):
        messageString: str = msg.payload.decode("utf-8")
        self.logger.info("Received message from topic {topic} with payload {payload}".format(topic=msg.topic,
                         payload=messageString))
        return json.loads(messageString)
