import daft
from typing import TypeVar, Generic, List, Type

from core.data.domain.base import DomainObject


class BaseAccessor(DomainObject):
    def __init__(self, df: daft.DataFrame):
        self.df = df

    def get_by_id(self, id: str, model: Type[T]) -> T:
        result = self.df.where(daft.col("id") == id).collect()
        if result:
            return model(**result[0])
        return None

    def get_all(self, model: Type[T]) -> List[T]:
        return [model(**row) for row in self.df.collect()]

    def insert(self, data: T):
        self.df = self.df.append(data.dict())

    def update(self, id: str, updates: dict):
        self.df = self.df.with_column(
            "data",
            daft.case([daft.col("id") == id], updates)
        )

    def delete(self, id: str):
        self.df = self.df.where(daft.col("id") != id)