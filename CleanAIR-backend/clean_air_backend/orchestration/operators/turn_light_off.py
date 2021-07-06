from orchestration.operators.operator import Operator


class TurnLightOffOperator(Operator):
    def execute(self):
        self.mqtt_client.publish("actuators/traffic-light", {"command": "GREEN"})
