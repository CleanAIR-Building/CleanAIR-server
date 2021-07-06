from data_processing.entities.carbon_dioxide_data import CarbonDioxideData
from data_processing.entities.infrared_data import InfraredData
from data_processing.entities.traffic_light_data import TrafficLightData
from data_processing.entities.window_state_data import WindowStateData
from data_processing.system_state import SystemState


class SystemStateMock(SystemState):
    def __init__(self):
        pass

    def update_carbon_dioxide_amount(self, update: CarbonDioxideData.CO2LEVEL):
        pass

    def update_infrared_data(self, update: InfraredData.TEMPERATURE):
        pass

    def update_traffic_light_state(self, update: TrafficLightData.LIGHT):
        pass

    def update_window_state(self, update: WindowStateData.WINDOW_STATE):
        pass

    def update_photo_electric_barrier_data(self, update: int):
        pass

    def _start_planning(self):
        pass

    def _create_building_state(self):
        pass
