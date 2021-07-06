from orchestration.operators.operator import Operator


class OpenWindowOperator(Operator):
    def execute(self):
        self.mqtt_client.publish("actuators/window", {"command": "OPEN"})
