from pydantic import Field, field_validator
import pyarrow as pa
import uuid
from typing import Optional, List

from core.

class User(DomainObject):
    # Domain-specific logic and validation
    user_id: str
    account_id: str
    project_id: str
    # Other fields and methods

class UserFactory:
    @staticmethod
    def create_from_data(data: Dict[str, Any]) -> UserDomainObject:
        # Logic to convert raw data into a UserDomainObject
        return UserDomainObject(**data)

class UserSelector:
    @staticmethod
    def by_account_id(account_id: str):
        # Define query logic based on account_id
        return f"SELECT * FROM users WHERE account_id = '{account_id}'"

class UserAccessor:
    def __init__(self, connection):
        self.connection = connection

    def get_users(self, account_id: str) -> List[UserDomainObject]:
        # Use the selector to define the query
        query = UserSelector.by_account_id(account_id)
        raw_data = self.connection.execute(query)  # Execute the query
        partitions = self.partition_data(raw_data)
        return [UserFactory.create_from_data(data) for data in partitions]

    def partition_data(self, data):
        # Implement partitioning logic
        # Partition by account_id, user_id, project_id, etc.
        return data  # Simplified for example

