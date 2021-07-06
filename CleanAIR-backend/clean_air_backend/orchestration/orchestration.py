from mqtt.mqtt_client import MQTTClient
from orchestration.operators.close_window import CloseWindowOperator
from orchestration.operators.open_window import OpenWindowOperator
from orchestration.operators.turn_light_off import TurnLightOffOperator
from orchestration.operators.turn_light_on import TurnLightOnOperator
import enum


class Orchestrator:
    class OperationName(enum.Enum):
        OPEN_WINDOW = 0,
        CLOSE_WINDOW = 1,
        TURN_LIGHT_ON = 2,
        TURN_LIGHT_OFF = 3,

    def __init__(self, mqttClient: MQTTClient):
        self.operators = {Orchestrator.OperationName.OPEN_WINDOW: OpenWindowOperator(mqttClient),
                          Orchestrator.OperationName.CLOSE_WINDOW: CloseWindowOperator(mqttClient),
                          Orchestrator.OperationName.TURN_LIGHT_ON: TurnLightOnOperator(mqttClient),
                          Orchestrator.OperationName.TURN_LIGHT_OFF: TurnLightOffOperator(mqttClient)}

    def execute(self, plan: list):
        parsed_plan = Orchestrator.__parse_plan(plan)
        for action in parsed_plan:
            self.operators[action].execute()

    @staticmethod
    def __parse_plan(plan: list):
        parsed_plan = []
        for action in plan:
            if "open-window" in action:
                parsed_plan.append(Orchestrator.OperationName.OPEN_WINDOW)
            elif "close-window" in action:
                parsed_plan.append(Orchestrator.OperationName.CLOSE_WINDOW)
            elif "turn-light-off" in action:
                parsed_plan.append(Orchestrator.OperationName.TURN_LIGHT_OFF)
            elif "turn-light-on" in action:
                parsed_plan.append(Orchestrator.OperationName.TURN_LIGHT_ON)
        return parsed_plan
