from planning.clean_air_building import BuildingState
from planning.smart_building_logic import SmartBuildingLogic
from .entities.carbon_dioxide_data import CarbonDioxideData
from .entities.infrared_data import InfraredData
from .entities.traffic_light_data import TrafficLightData
from .entities.window_state_data import WindowStateData
from .entities.photoelectric_data import PhotoElectricBarrierData


class SystemState:
    def __init__(self, smart_building_logic: SmartBuildingLogic):
        self.carbon_dioxide_amount: CarbonDioxideData.CO2LEVEL = CarbonDioxideData.CO2LEVEL.LOW
        self.infrared_data: InfraredData.TEMPERATURE = InfraredData.TEMPERATURE.COLD
        self.traffic_light_state: TrafficLightData.LIGHT = TrafficLightData.LIGHT.GREEN
        self.window_state: WindowStateData.WINDOW_STATE = WindowStateData.WINDOW_STATE.CLOSED
        self.photo_electric_barrier_data: PhotoElectricBarrierData.OCCUPANCY_STATE = PhotoElectricBarrierData.OCCUPANCY_STATE.NOT_FULL
        self.smart_building_logic = smart_building_logic

    def update_carbon_dioxide_amount(self, update: CarbonDioxideData.CO2LEVEL):
        if self.carbon_dioxide_amount != update:
            self.carbon_dioxide_amount = update
            self._start_planning()

    def update_infrared_data(self, update: InfraredData.TEMPERATURE):
        if self.infrared_data != update:
            self.infrared_data = update
            self._start_planning()

    def update_traffic_light_state(self, update: TrafficLightData.LIGHT):
        if self.traffic_light_state != update:
            self.traffic_light_state = update
            self._start_planning()

    def update_window_state(self, update: WindowStateData.WINDOW_STATE):
        if self.window_state != update:
            self.window_state = update
            self._start_planning()

    def update_photo_electric_barrier_data(self, update: PhotoElectricBarrierData.OCCUPANCY_STATE):
        if self.photo_electric_barrier_data != update:
            self.photo_electric_barrier_data = update
            self._start_planning()

    def _start_planning(self):
        building_state = self._create_building_state()
        self.smart_building_logic.plan(building_state)

    def _create_building_state(self):
        building_full: bool = self.photo_electric_barrier_data == PhotoElectricBarrierData.OCCUPANCY_STATE.FULL
        infection_positive: bool = self.infrared_data == InfraredData.TEMPERATURE.HOT
        window_open: bool = self.window_state == WindowStateData.WINDOW_STATE.OPEN
        bad_air: bool = self.carbon_dioxide_amount == CarbonDioxideData.CO2LEVEL.HIGH
        traffic_light_red: bool = self.traffic_light_state == TrafficLightData.LIGHT.RED
        return BuildingState(building_full=building_full, infection_positive=infection_positive, window_open=window_open, bad_air=bad_air, traffic_light_red=traffic_light_red)
