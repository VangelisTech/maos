from typing import Optional, List
from pydantic import EmailStr, Field
from src.core.data.schema.base import DomainObject, DomainFactory, DomainSelector, DomainObjectAccessor
from api.config import Config

class User(DomainObject):
    account_id: str = Field(..., description="Account ID associated with the user")
    project_id: str = Field(..., description="Project ID associated with the user")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    is_active: bool = Field(default=True, description="User's active status")

    class Meta:
        type: str = "User"

class UserFactory(DomainFactory[User]):
    @staticmethod
    def create_new_user(account_id: str, project_id: str, email: str, name: str) -> User:
        return User.create_new(
            account_id=account_id,
            project_id=project_id,
            email=email,
            name=name
        )

class UserSelector(DomainSelector):
    @staticmethod
    def by_email(email: str) -> str:
        return f"{UserSelector.base_query('users')} WHERE email = '{email}'"

class UserAccessor(DomainObjectAccessor):
    def __init__(self, config: Config):
        super().__init__(config)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = UserSelector.by_email(email)
        df = self.config.daft().sql(query)
        if df.count().collect()[0] > 0:
            user_data = df.collect().to_pydict()[0]
            return UserFactory.create_from_data(user_data, "User")
        return None

    async def get_active_users(self) -> List[User]:
        return await self.query("users", "User", ["is_active = TRUE"])