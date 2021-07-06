from src.planning.smart_building_logic import BuildingState, SmartBuildingLogic

def main():
    sbl = SmartBuildingLogic(BuildingState())
    sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True))

if __name__=='__main__':
    main()