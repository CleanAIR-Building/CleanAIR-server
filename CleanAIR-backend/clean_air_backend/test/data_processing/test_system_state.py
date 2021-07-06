#! bin/python3
from data_processing.entities.carbon_dioxide_data import CarbonDioxideData
from data_processing.entities.infrared_data import InfraredData
from data_processing.entities.traffic_light_data import TrafficLightData
from data_processing.entities.window_state_data import WindowStateData
from data_processing.entities.photoelectric_data import PhotoElectricBarrierData
from data_processing.system_state import SystemState
from planning.clean_air_building import BuildingState
from test.utils.smart_building_logic_mock import SmartBuildingLogicMock
import unittest


class test_system_state(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.sbl = SmartBuildingLogicMock()
        self.system_state: SystemState = SystemState(self.sbl)

    def tearDown(self):
        pass

    def test_update_carbon_dioxide_amount(self):
        self.assertEqual(CarbonDioxideData.CO2LEVEL.LOW, self.system_state.carbon_dioxide_amount)
        self.system_state.update_carbon_dioxide_amount(CarbonDioxideData.CO2LEVEL.HIGH)
        self.assertEqual(CarbonDioxideData.CO2LEVEL.HIGH, self.system_state.carbon_dioxide_amount)

    def test_update_infrared_data(self):
        self.assertEqual(InfraredData.TEMPERATURE.COLD, self.system_state.infrared_data)
        self.system_state.update_infrared_data(InfraredData.TEMPERATURE.HOT)
        self.assertEqual(InfraredData.TEMPERATURE.HOT, self.system_state.infrared_data)

    def test_update_traffic_light_state(self):
        self.assertEqual(TrafficLightData.LIGHT.GREEN, self.system_state.traffic_light_state)
        self.system_state.update_traffic_light_state(TrafficLightData.LIGHT.RED)
        self.assertEqual(TrafficLightData.LIGHT.RED, self.system_state.traffic_light_state)

    def test_update_window_state(self):
        self.assertEqual(WindowStateData.WINDOW_STATE.CLOSED, self.system_state.window_state)
        self.system_state.update_window_state(WindowStateData.WINDOW_STATE.OPEN)
        self.assertEqual(WindowStateData.WINDOW_STATE.OPEN, self.system_state.window_state)

    def test_update_photo_electric_barrier_data(self):
        self.assertEqual(PhotoElectricBarrierData.OCCUPANCY_STATE.NOT_FULL,
                         self.system_state.photo_electric_barrier_data)
        self.system_state.update_photo_electric_barrier_data(PhotoElectricBarrierData.OCCUPANCY_STATE.FULL)
        self.assertEqual(PhotoElectricBarrierData.OCCUPANCY_STATE.FULL, self.system_state.photo_electric_barrier_data)

    def test_create_building_state(self):
        expected_building_state: BuildingState = BuildingState()
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)

        self.system_state.photo_electric_barrier_data = PhotoElectricBarrierData.OCCUPANCY_STATE.FULL
        expected_building_state.building_full = True
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)

        self.system_state.infrared_data = InfraredData.TEMPERATURE.HOT
        expected_building_state.infection_positive = True
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)

        self.system_state.window_state = WindowStateData.WINDOW_STATE.OPEN
        expected_building_state.window_open = True
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)

        self.system_state.carbon_dioxide_amount = CarbonDioxideData.CO2LEVEL.HIGH
        expected_building_state.bad_air = True
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)

        self.system_state.traffic_light_state = TrafficLightData.LIGHT.RED
        expected_building_state.traffic_light_red = True
        actual_building_state: BuildingState = self.system_state._create_building_state()
        self.assertEqual(expected_building_state, actual_building_state)


if __name__ == "__main__":
    unittest.main()
