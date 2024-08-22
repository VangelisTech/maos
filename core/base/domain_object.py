import pyarrow as pa
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, HttpUrl, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
import uuid
import ulid
from datetime import datetime, date, time


class DomainObjectError(Exception):
    """Base exception class for CustomModel errors."""


class ULIDValidationError(CustomModelError):
    """Raised when ULID validation fails."""


class DomainObject(BaseModel):
    """
    A versatile Pydantic BaseModel with extended functionality.

    Attributes:
      id            │ ULID Unique identifier
      updated_at    │ UTC timestamp of update
      metadata      │ Additional metadata dict
    ─────────────────────────────────────────────
    Properties:
      created_at    │ Timestamp from ULID
    ─────────────────────────────────────────────
    Methods:
      update_timestamp()  │   Update 'updated_at'
      create_new(**data)  │   New instance with ULID
    ─────────────────────────────────────────────
    Usage:
      class MyModel(CustomModel):
          field1: str
          field2: int

      model = MyModel(field1="test", field2=42)
      new_model = MyModel.create_new(field1="new")
    ─────────────────────────────────────────────
    Notes:
      • Inherits from Pydantic BaseModel
      • Uses ULID for unique identification
      • Supports automatic timestamp management
      • Can be extended with Arrow/Spark via
        @with_arrow and @with_spark decorators
    ______________________________________________

    """

    id: pa.string() = Field(
        default_factory= lambda: ulid.new().str,
        description="ULID Unique identifier"
    )
    updated_at: Optional[pa.timestamp()] = Field(
        default=None,
        description="UTC timestamp of last update"
    )
    metadata: Optional[Dict[pa.string(), pa.any()]] = Field(
        default_factory=,
        description="Additional metadata"
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
            bytes: lambda v: v.decode('utf-8', errors='ignore'),
            uuid.UUID: str,
            ulid.ULID: str,
            HttpUrl: str,
            EmailStr: str,
            PhoneNumber: str
        }
        allow_population_by_field_name = True
        use_enum_values = True

    @field_validator('id')
    def validate_ulid(cls, v):
        try:
            ulid.parse(v)
            return v
        except ValueError as e:
            raise ULIDValidationError(f"Invalid ULID: {v}") from e

    @property
    def created_at(self) -> datetime:
        try:
            return ulid.parse(self.id).timestamp().datetime
        except ValueError as e:
            raise ULIDValidationError(f"Invalid ULID: {self.id}") from e

    def update_timestamp(self):
        self.updated_at = datetime.now(datetime.timezone.utc)

    @classmethod
    def create_new(cls, **data) -> 'DomainObject':
        """Create a new instance with a fresh ULID and current timestamp."""
        return cls(id=ulid.new().str, updated_at=datetime.now(datetime.timezone.utc), **data)
