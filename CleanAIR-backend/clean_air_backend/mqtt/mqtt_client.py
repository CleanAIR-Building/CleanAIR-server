from data_processing.consumers.consumer import Consumer
import logging
import paho.mqtt.client as mqtt
import json

logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self, client_name: str, user: str, password: str, host: str, port: int = 1883, keepalive: int = 60,
                 consumers=None):
        if consumers is None:
            consumers = []

        self.client_name: str = client_name
        self.host: str = host
        self.port: int = port
        self.user = user
        self.password = password
        self.keepalive: int = keepalive
        self.client: mqtt.Client = mqtt.Client(self.client_name)
        self.client.username_pw_set(self.user, self.password)
        self.consumers: list = consumers
        # self.client.on_message = lambda client, userdata, msg: self.consumers[msg.topic].consume(msg)
        self.client.on_connect = lambda client, userdata, flags, rc: print("Connected With Result Code: {}".format(rc))
        self.client.on_message = lambda client, userdata, msg: logger.info("Received {msg} from topic: {topic}",
                                                                           msg=msg.payload.decode("utf-8"),
                                                                           topic=msg.topic)

    def connect(self):
        self.client.connect(self.host, port=self.port, keepalive=self.keepalive)
        for consumer in self.consumers:
            self.client.subscribe(consumer.topic)

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload))

    def start(self):
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()

    def add_consumer(self, *consumers: Consumer):
        for consumer in consumers:
            self.consumers.append(consumer)
            self.client.message_callback_add(consumer.topic, consumer.consume)
