"""
This module encapsulates the logic of the clean air bulding.
In order to issue AI planning with PDDL, this module makes use of the clean_air_building module which defines the domain and problem instances.
"""

import requests

from orchestration.orchestration import Orchestrator
from planning.clean_air_building import CleanAIRBuildingDomain, CleanAIRProblem, BuildingState
import logging

logger = logging.getLogger(__name__)

class SmartBuildingLogic:
    """
    Holds the current state of the Clean Air Building and offers AI planning functionality.
    """

    def __init__(self, initial_state: BuildingState, orchestrator: Orchestrator):
        """
        :param initial_state: The initial state of the building.
        """
        self.last_state = initial_state
        self.pddl_domain = CleanAIRBuildingDomain().generate_domain_pddl()
        self.orchestrator = orchestrator

    def plan(self, building_state: BuildingState):
        """
        Issues the AI planning by creating a pddl problem instance depending on the given param:
        :param building_state: the building state is used to create the pddl problem instance.
        If the state of the buidling does not change, no action is taken.
        :raises requests.RequestException: if the webservice used for solving the planning problems is not available.
        
        If the building state changes, and a plan was retrieved from the solver webservice, the plan will be handed over to the orchestration component.
        """
        logger.debug(building_state)
        # If the state is unchanged from the last call, don't do anything
        if self.last_state == building_state:
            logger.debug("Nothing to plan - the state is unchanged.")
            return

        self.last_state = building_state
        pddl_problem = CleanAIRProblem(building_state).generate_problem_pddl()
        plan = self.__send_request_to_solver(pddl_problem)
        self.orchestrator.execute(plan)

    def __send_request_to_solver(self, pddl_problem: str):
        """
        Returns a plan for the given pddl problem from the solver.
        :param pddl_problem: The problem to be solved
        :return: a plan, i.e., a list of actions to be taken to reach the goal state.
        """
        data = {
            'domain': self.pddl_domain,
            'problem': pddl_problem
        }
        logger.debug(f"The problem model is: {pddl_problem}")

        response = requests.post('http://solver.planning.domains/solve', verify=False, json=data)

        if response.status_code != 200:
            raise requests.RequestException("Webservice unavailable!")
        else:
            return self.__retrieve_plan(response)

    def __retrieve_plan(self, response):
        """
        Retrieves the plan, i.e., a list of actions, from the response of the solver webservice.
        """
        plan = []
        if response.json()['status'] == 'error':
            # print("No action has to be taken: ", response.json()['result']['output'])
            # no action necessary
            pass
        else:
            pddl_plan = response.json()['result']['plan']
            for action in pddl_plan:
                plan.append(action['name'])
        logger.debug(f"The plan is: {plan}")
        return plan
