from orchestration.operators.operator import Operator


class CloseWindowOperator(Operator):
    def execute(self):
        self.mqtt_client.publish("actuators/window", {"command": "CLOSE"})
