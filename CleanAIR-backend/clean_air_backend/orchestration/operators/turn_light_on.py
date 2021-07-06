from orchestration.operators.operator import Operator


class TurnLightOnOperator(Operator):
    def execute(self):
        self.mqtt_client.publish("actuators/traffic-light", {"command": "RED"})
