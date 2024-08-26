from enum import Enum
from typing import List, Dict

class ResourceType(Enum):
    DATABASE = 1
    API = 2
    FILE_SYSTEM = 3

class AccessLevel(Enum):
    READ = 1
    WRITE = 2
    EXECUTE = 3

class IAMRole:
    def __init__(self, name: str, permissions: Dict[ResourceType, AccessLevel]):
        self.name = name
        self.permissions = permissions

class RowLevelPolicy:
    def __init__(self, resource: str, condition: str):
        self.resource = resource
        self.condition = condition

class AgentAccessControl:
    def __init__(self, agent_id: str, iam_role: IAMRole, row_level_policies: List[RowLevelPolicy]):
        self.agent_id = agent_id
        self.iam_role = iam_role
        self.row_level_policies = row_level_policies

    def can_access(self, resource_type: ResourceType, access_level: AccessLevel) -> bool:
        return self.iam_role.permissions.get(resource_type, AccessLevel.READ) >= access_level

    def get_row_level_policy(self, resource: str) -> str:
        for policy in self.row_level_policies:
            if policy.resource == resource:
                return policy.condition
        return "1=1"  # Default to allow all if no specific policy

class AccessControlSystem:
    def __init__(self):
        self.agent_access_controls: Dict[str, AgentAccessControl] = {}

    def register_agent(self, agent_access_control: AgentAccessControl):
        self.agent_access_controls[agent_access_control.agent_id] = agent_access_control

    def check_access(self, agent_id: str, resource_type: ResourceType, access_level: AccessLevel) -> bool:
        if agent_id not in self.agent_access_controls:
            return False
        return self.agent_access_controls[agent_id].can_access(resource_type, access_level)

    def get_row_level_policy(self, agent_id: str, resource: str) -> str:
        if agent_id not in self.agent_access_controls:
            return "1=0"  # No access by default
        return self.agent_access_controls[agent_id].get_row_level_policy(resource)

# Example usage
iam_role = IAMRole("data_analyst", {
    ResourceType.DATABASE: AccessLevel.READ,
    ResourceType.API: AccessLevel.EXECUTE
})

row_level_policies = [
    RowLevelPolicy("users_table", "department = 'Sales'"),
    RowLevelPolicy("orders_table", "region = 'North America'")
]

agent_access = AgentAccessControl("agent_001", iam_role, row_level_policies)

access_system = AccessControlSystem()
access_system.register_agent(agent_access)

# Check if agent can read from database
print(access_system.check_access("agent_001", ResourceType.DATABASE, AccessLevel.READ))  # True

# Get row-level policy for users_table
print(access_system.get_row_level_policy("agent_001", "users_table"))  # "department = 'Sales'"