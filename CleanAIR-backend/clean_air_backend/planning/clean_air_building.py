"""
This file makes use of the py2pddl libarary to define the pddl domain and enable dynamic creation of problem instances
depending on the state of the building.
"""
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class BuildingState:

    def __init__(self, building_full: bool = False, infection_positive: bool = False, window_open: bool = False,
                 bad_air: bool = False, traffic_light_red: bool = False):
        """
        Captures the state of the SmartAIRBuilding to be handed over to the Smart Building Logic.
        [ALL PARAMS ARE OPTIONAL AND DEFAULT TO FALSE]
        :param building_full: true if the limit of people in the building is reached
        :param infection_positive: true if the infrared sensor detects a potential infection
        :param window_open: true if the window is open
        :param bad_air: true if the air quality in the building is bad
        :param traffic_light_red: true if the traffic light is turned red
        """
        self.building_full = building_full
        self.infection_positive = infection_positive
        self.window_open = window_open
        self.bad_air = bad_air
        self.traffic_light_red = traffic_light_red

    def __eq__(self, o: object) -> bool:
        if (isinstance(o, BuildingState)):
            return self.building_full == o.building_full and self.infection_positive == o.infection_positive and self.window_open == o.window_open and self.bad_air == o.bad_air and self.traffic_light_red == o.traffic_light_red
        else:
            return False

    def __str__(self):
        return f"BUILDING STATE: building_full={self.building_full} | infection_positive={self.infection_positive} | window_open={self.window_open} | bad_air={self.bad_air} | traffic_light_red={self.traffic_light_red}"


class CleanAIRBuildingDomain(Domain):
    """
    Defines the pddl domain programmatically, hence it defines all types, predicates and actions.
    This class is completely specified - it will not be altered at runtime and serves to create domain files as well as
    (by inheritence) corresponding problem files.
    """

    Building = create_type("Building")
    Window = create_type("Window")
    TrafficLight = create_type("TrafficLight")
    InfectionScanner = create_type("InfectionScanner")

    @predicate(Building)
    def good_air(self, b):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Building)
    def full(self, b):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Window)
    def open(self, w):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(TrafficLight)
    def turned_on(self, t):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(InfectionScanner)
    def positive(self, i):
        """Complete the method signature and specify
        the respective types in the decorator"""

    @predicate(Building)
    def placeholder(self, b):
        """This is a placeholder because empty initial states are not allowed in PDDL, even though there is the close world assumption.
        Who tf invented this!? How are you supposed to model states where no predicate is true if you have to give at least one true predicate?
        This is why we need this meaningless placeholder which is used whenever the initial state actually consists of only false predicates."""

    @action(Building, Window)
    def open_window(self, b, w):
        precond = [~self.open(w)]
        effect = [self.good_air(b), self.open(w)]
        return precond, effect

    @action(Building, Window)
    def close_window(self, b, w):
        precond = [self.good_air(b), self.open(w)]
        effect = [~self.good_air(b), ~self.open(w)]
        return precond, effect

    @action(Building, InfectionScanner, TrafficLight)
    def turn_light_off(self, b, i, t):
        precond = [self.good_air(b), ~self.full(b), ~self.positive(i), self.turned_on(t)]
        effect = [~self.turned_on(t)]
        return precond, effect

    @action(Building, TrafficLight)
    def turn_light_on_full(self, b, t):
        precond = [self.full(b), ~self.turned_on(t)]
        effect = [self.turned_on(t)]
        return precond, effect

    @action(InfectionScanner, TrafficLight)
    def turn_light_on_infection(self, i, t):
        precond = [self.positive(i), ~self.turned_on(t)]
        effect = [self.turned_on(t)]
        return precond, effect

    @action(Building, TrafficLight)
    def turn_light_on_air(self, b, t):
        precond = [~self.good_air(b), ~self.turned_on(t)]
        effect = [self.good_air(b), self.turned_on(t)]
        return precond, effect


class CleanAIRProblem(CleanAIRBuildingDomain):
    """
    Models a pddl problem instance for the clean air building domain.
    This class can be instantiated with a BuildingsState-object to dynamically create pddl problem files.
    """

    def __init__(self, state: BuildingState):
        """
        Instantiate a problem instance for the clean air building domain with the corresponding :param state: BuildingState-object.
        """
        super().__init__()
        self.buildings = CleanAIRBuildingDomain.Building.create_objs(["b"])
        self.windows = CleanAIRBuildingDomain.Window.create_objs(["w"])
        self.traffic_lights = CleanAIRBuildingDomain.TrafficLight.create_objs(["t"])
        self.infection_scanners = CleanAIRBuildingDomain.InfectionScanner.create_objs(["i"])

        self.b = self.buildings["b"]
        self.w = self.windows["w"]
        self.t = self.traffic_lights["t"]
        self.i = self.infection_scanners["i"]

        self.state = state

    @init
    def init(self):
        """
        Defines the initial state depending on the BuildingState-object the problem was instaciated with.
        """
        initial_state = []

        if self.state.building_full:
            initial_state.append(self.full(self.b))
        if not self.state.bad_air:
            initial_state.append(self.good_air(self.b))
        if self.state.window_open:
            initial_state.append(self.open(self.w))
        if self.state.infection_positive:
            initial_state.append(self.positive(self.i))
        if self.state.traffic_light_red:
            initial_state.append(self.turned_on(self.t))

        if not initial_state:
            initial_state.append(self.placeholder(self.b))

        return initial_state

    @goal
    def goal(self):
        """
        Defines the goal state depending on the BuildingState-object the problem was instaciated with.
        """
        goal_state = []

        if self.state.bad_air:
            goal_state.append(self.good_air(self.b))
            goal_state.append(self.open(self.w))
        elif self.state.window_open:  # if the air is good, but the window is open
            goal_state.append(~self.open(self.w))

        if self.state.building_full or self.state.infection_positive or self.state.bad_air:
            goal_state.append(self.turned_on(self.t))
        else:
            goal_state.append(~self.turned_on(self.t))

        return goal_state
