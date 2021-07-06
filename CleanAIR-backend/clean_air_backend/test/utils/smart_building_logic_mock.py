from planning.clean_air_building import BuildingState
from planning.smart_building_logic import SmartBuildingLogic


class SmartBuildingLogicMock(SmartBuildingLogic):
    def __init__(self):
        pass

    def plan(self, building_state: BuildingState):
        pass
