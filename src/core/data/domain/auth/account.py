from typing import Optional
from pydantic import Field
from src.core.data.schema.base import DomainObject, DomainFactory, DomainSelector, DomainObjectAccessor
from api.config import Config

class Account(DomainObject):
    name: str = Field(..., description="Account name")
    owner_id: str = Field(..., description="User ID of the account owner")
    is_active: bool = Field(default=True, description="Account active status")

    class Meta:
        type: str = "Account"

class AccountFactory(DomainFactory[Account]):
    @staticmethod
    def create_new_account(name: str, owner_id: str) -> Account:
        return Account.create_new(
            name=name,
            owner_id=owner_id
        )

class AccountSelector(DomainSelector):
    @staticmethod
    def by_owner_id(owner_id: str) -> str:
        return f"{AccountSelector.base_query('accounts')} WHERE owner_id = '{owner_id}'"

class AccountAccessor(DomainObjectAccessor):
    def __init__(self, config: Config):
        super().__init__(config)

    async def get_account_by_owner(self, owner_id: str) -> Optional[Account]:
        query = AccountSelector.by_owner_id(owner_id)
        df = self.config.daft().sql(query)
        if df.count().collect()[0] > 0:
            account_data = df.collect().to_pydict()[0]
            return AccountFactory.create_from_data(account_data, "Account")
        return None