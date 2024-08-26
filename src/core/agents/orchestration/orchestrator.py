from src.core.utils.plugin_loader import load_plugin

class Orchestrator:
    def __init__(self, planning_strategy='adaptive_multi_stage'):
        plugin = load_plugin(planning_strategy)
        self.planner = plugin.AdaptiveMultiStagePlanningPlugin().get_planner()

    def orchestrate(self, context, goals):
        plan = self.planner.plan(context, goals)
        # Rest of the orchestration logic