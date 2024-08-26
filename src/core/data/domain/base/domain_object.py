from typing import TypeVar, Type, Dict, Any, List, Optional, ClassVar, Generic
from pydantic import BaseModel, Field
import ulid
from datetime import datetime
import daft
import importlib
import inspect
from api.config import config

T = TypeVar('T', bound='DomainObject')

class DomainObjectError(Exception):
    """Base exception class for CustomModel errors."""

class ULIDValidationError(DomainObjectError):
    """Raised when ULID validation fails."""

class DomainObject(BaseModel):
    id: str = Field(default_factory=lambda: ulid.new().str, description="ULID Unique identifier")
    updated_at: Optional[datetime] = Field(default=None, description="UTC timestamp of last update")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        arbitrary_types_allowed = True

    class Meta:
        type: ClassVar[str] = "DomainObject"

    @property
    def created_at(self) -> datetime:
        return ulid.parse(self.id).timestamp().datetime

    def update_timestamp(self):
        self.updated_at = datetime.now(datetime.timezone.utc)

    @classmethod
    def create_new(cls: Type[T], **data) -> T:
        return cls(id=ulid.new().str, updated_at=datetime.now(datetime.timezone.utc), **data)

class DomainFactory(Generic[T]):
    @staticmethod
    def create_from_data(data: Dict[str, Any], object_type: str) -> T:
        class_type = DomainFactory.get_class_by_type(object_type)
        return class_type(**data)

    @staticmethod
    def create_new(object_type: str, **data) -> T:
        class_type = DomainFactory.get_class_by_type(object_type)
        return class_type.create_new(**data)

    @staticmethod
    def get_class_by_type(object_type: str) -> Type[T]:
        for name, obj in inspect.getmembers(importlib.import_module(__name__)):
            if inspect.isclass(obj) and issubclass(obj, DomainObject) and hasattr(obj.Meta, 'type'):
                if obj.Meta.type == object_type:
                    return obj
        raise ValueError(f"Unknown object type: {object_type}")

class DomainSelector:
    @staticmethod
    def base_query(table_name: str) -> str:
        return f"SELECT * FROM {table_name}"

    @staticmethod
    def by_id(table_name: str, id: str) -> str:
        return f"{DomainSelector.base_query(table_name)} WHERE id = '{id}'"

    @staticmethod
    def build_query(table_name: str, conditions: List[str] = None) -> str:
        query = DomainSelector.base_query(table_name)
        if conditions:
            where_clause = " AND ".join(conditions)
            query += f" WHERE {where_clause}"
        return query

class DomainObjectAccessor:
    async def get_table_location(self, table_name: str) -> str:
        table_info = await config.unity_catalog().tables.retrieve(table_name)
        return table_info.location

    async def get_dataframe(self, table_name: str, object_type: str) -> daft.DataFrame:
        table_location = await self.get_table_location(table_name)
        df = config.daft().from_iceberg(table_location)
        return df.where(df["_type"] == object_type)

    @classmethod
    async def get_by_id(cls, id: str) -> Optional[T]:
        # Extract timestamp from ULID
        timestamp = ulid.parse(id).timestamp().datetime

        # Create a time range for efficient querying
        start_time = timestamp - timedelta(minutes=1)  # Adjust as needed
        end_time = timestamp + timedelta(minutes=1)  # Adjust as needed

        query = f"""
            SELECT * FROM {cls.get_table_name()}
            WHERE id = '{id}'
            AND _type = '{cls.get_object_type()}'
            AND created_at BETWEEN '{start_time}' AND '{end_time}'
            """

        df = config.daft().sql(query)
        if df.count().collect()[0] > 0:
            object_data = df.collect().to_pydict()[0]
            return cls.create_from_data(object_data)
        return None

    async def query(self, table_name: str, object_type: str, conditions: List[str] = None) -> List[T]:
        query = DomainSelector.build_query(table_name, conditions)
        df = config.daft().sql(query)
        objects_df = df.collect()
        return [DomainFactory.create_from_data(data, object_type) for data in objects_data]

    async def create(self, table_name: str, object_type: str, **data) -> T:
        new_object = DomainFactory.create_new(object_type, **data)
        # Implement Iceberg table insertion logic here
        return new_object

    async def update(self, table_name: str, obj: T) -> T:
        obj.update_timestamp()
        # Implement Iceberg table update logic here
        return obj

    async def delete(self, table_name: str, id: str, object_type: str) -> bool:
        # Implement Iceberg table deletion logic here
        return True