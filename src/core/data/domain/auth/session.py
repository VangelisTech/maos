from typing import Optional
from pydantic import Field
from src.core.data.schema.base import DomainObject, DomainFactory, DomainSelector, DomainObjectAccessor
from api.config import get_config
from datetime import datetime

class UserSession(DomainObject):
    user_id: str = Field(..., description="User ID associated with the session")
    token: str = Field(..., description="Session token")
    expires_at: datetime = Field(..., description="Session expiration time")

    class Meta:
        type: str = "UserSession"

class UserSessionFactory(DomainFactory[UserSession]):
    @staticmethod
    def create_new_session(user_id: str, token: str, expires_at: datetime) -> UserSession:
        return UserSession.create_new(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )

class UserSessionSelector(DomainSelector):
    @staticmethod
    def by_token(token: str) -> str:
        return f"{UserSessionSelector.base_query('user_sessions')} WHERE token = '{token}'"

class UserSessionAccessor(DomainObjectAccessor):
    def __init__(self, config: Config):
        super().__init__(config)

    async def get_session_by_token(self, token: str) -> Optional[UserSession]:
        query = UserSessionSelector.by_token(token)
        df = self.config.daft().sql(query)
        if df.count().collect()[0] > 0:
            session_data = df.collect().to_pydict()[0]
            return UserSessionFactory.create_from_data(session_data, "UserSession")
        return None