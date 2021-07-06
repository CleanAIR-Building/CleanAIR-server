from orchestration.orchestration import Orchestrator
from planning.clean_air_building import BuildingState
from planning.smart_building_logic import SmartBuildingLogic
import unittest


class test_smart_building_logic(unittest.TestCase):
    class OrchestratorMockBase(Orchestrator):
        def __init__(self, test_case):
            self.test_case = test_case

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_plan_one_true(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-air b t)', '(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True))

    def test_plan_three_true(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)', '(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True))

    def test_plan_all_true(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True, window_open=True,
                               traffic_light_red=True))

    def test_plan_all_false(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(bad_air=True), OrchestratorMock(self))
        sbl.plan(BuildingState())

    def test_plan_1(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-air b t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True, window_open=True,
                               traffic_light_red=False))

    def test_plan_2(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True, window_open=False,
                               traffic_light_red=True))

    def test_plan_3(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=False, window_open=True,
                               traffic_light_red=True))

    def test_plan_4(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=False, building_full=True, window_open=True,
                               traffic_light_red=True))

    def test_plan_5(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=True, window_open=True,
                               traffic_light_red=True))

    def test_plan_10(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)', '(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=True, window_open=False,
                               traffic_light_red=False))

    def test_plan_11(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-air b t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=False, window_open=True,
                               traffic_light_red=False))

    def test_plan_12(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-air b t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=False, building_full=True, window_open=True,
                               traffic_light_red=False))

    def test_plan_13(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)', '(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=True, window_open=True,
                               traffic_light_red=False))

    def test_plan_14(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=True, window_open=False,
                               traffic_light_red=True))

    def test_plan_15(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=False, window_open=True,
                               traffic_light_red=True))

    def test_plan_16(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=True, window_open=True,
                               traffic_light_red=True))

    def test_plan_17(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=False, building_full=False, window_open=True,
                               traffic_light_red=True))

    def test_plan_18(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=False, window_open=False,
                               traffic_light_red=True))

    def test_plan_19(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=False, building_full=True, window_open=False,
                               traffic_light_red=True))

    def test_plan_100(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(open-window b w)', '(turn-light-on-infection i t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=True, building_full=False, window_open=False,
                               traffic_light_red=False))

    def test_plan_101(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(open-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=True, infection_positive=False, building_full=False, window_open=False,
                               traffic_light_red=True))

    def test_plan_102(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-off b i t)', '(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=False, window_open=True,
                               traffic_light_red=True))

    def test_plan_103(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                # expect that no action has to be taken - just wait.
                expected_plan: list = []
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=False, window_open=False,
                               traffic_light_red=True))

    def test_plan_104(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=True, window_open=False,
                               traffic_light_red=False))

    def test_plan_105(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)', '(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=False, window_open=True,
                               traffic_light_red=False))

    def test_plan_106(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-full b t)', '(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=True, window_open=True,
                               traffic_light_red=False))

    def test_plan_1000(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-infection i t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=True, building_full=False, window_open=False,
                               traffic_light_red=False))

    def test_plan_1001(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-on-full b t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=True, window_open=False,
                               traffic_light_red=False))

    def test_plan_1002(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(close-window b w)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=False, window_open=True,
                               traffic_light_red=False))

    def test_plan_1003(self):
        class OrchestratorMock(test_smart_building_logic.OrchestratorMockBase):
            def execute(self, plan: list):
                expected_plan: list = ['(turn-light-off b i t)']
                self.test_case.assertCountEqual(expected_plan, plan)

        sbl = SmartBuildingLogic(BuildingState(), OrchestratorMock(self))
        sbl.plan(BuildingState(bad_air=False, infection_positive=False, building_full=False, window_open=False,
                               traffic_light_red=True))

if __name__ == "__main__":
    unittest.main()
