from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.core.data.schema.base import DomainObject, User
class BasePlanner(DomainObject):
    @abstractmethod
    def plan(self, context: Dict[str, Any], goals: List[str]) -> Plan:
        """
        Generate a plan based on the given context and goals.

        :param context: Dictionary containing relevant context information
        :param goals: List of goals to be achieved
        :return: A Plan object detailing the steps to achieve the goals
        """
        pass

    @abstractmethod
    def execute_step(self, step: PlanStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step of the plan.

        :param step: The PlanStep to be executed
        :param context: Current context information
        :return: Updated context after step execution
        """
        pass

    def execute_plan(self, plan: Plan) -> Dict[str, Any]:
        """
        Execute an entire plan.

        :param plan: The Plan to be executed
        :return: Final context after plan execution
        """
        context = plan.context
        for step in plan.steps:
            context = self.execute_step(step, context)
        return context