import json
import uuid
from datetime import datetime, date, time
from typing import Any, Dict, Optional, ClassVar

import ulid
from pydantic import HttpUrl, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, TimestampType, MapType, IntegerType, \
    FloatType, BinaryType, DateType


class SparkConversionError(CustomModelError):
    """Raised when conversion to/from Spark fails."""

def with_spark(use_arrow: bool = False):
     """
    Add Spark serialization to CustomModel subclass.
    ┌─────────────────────────────────────────────┐
    │ Arg: use_arrow=False (bool)                 │
    │      Use Arrow for Spark operations         │
    ├─────────────────────────────────────────────┤
    │ Methods:                                    │
    │  to_spark_row() │ Instance → Spark Row      │
    │  from_spark_row()│ Spark Row → Instance     │
    │  get_spark_schema()│ Get Spark schema       │
    ├─────────────────────────────────────────────┤
    │ Usage: @with_spark(use_arrow=True)          │
    │        class MyModel(CustomModel): ...      │
    ├─────────────────────────────────────────────┤
    │ Notes: • Enables Spark DataFrame integration│
    │        • Apply after @with_arrow if both    │
    │        • Handle SparkConversionError        │
    └─────────────────────────────────────────────┘
    """
    def decorator(cls):
        @functools.wraps(cls)
        class SparkWrapper(cls):
            _spark_schema: ClassVar[Optional[StructType]] = None

            def to_spark_row(self, spark: SparkSession):
                try:
                    if use_arrow and hasattr(self, 'to_arrow'):
                        # Use Arrow as an intermediate format
                        arrow_table = self.to_arrow()
                        return spark.createDataFrame(arrow_table.to_pandas()).first()
                    else:
                        # Fallback to direct conversion
                        data = self.dict()
                        for key, value in data.items():
                            if isinstance(value, (datetime, date, time, uuid.UUID, ulid.ULID, EmailStr, PhoneNumber)):
                                data[key] = str(value)
                            elif isinstance(value, (dict, list)):
                                data[key] = json.dumps(value)
                        return spark.createDataFrame([data]).first()
                except Exception as e:
                    raise SparkConversionError(f"Error converting to Spark Row: {str(e)}") from e

            @classmethod
            def from_spark_row(cls, row) -> 'CustomModel':
                try:
                    data = row.asDict()
                    for field_name, field_type in cls.__annotations__.items():
                        if field_name in data:
                            if field_type == datetime:
                                data[field_name] = datetime.fromisoformat(data[field_name])
                            elif field_type == date:
                                data[field_name] = date.fromisoformat(data[field_name])
                            elif field_type == time:
                                data[field_name] = time.fromisoformat(data[field_name])
                            elif field_type in (Dict[str, Any], List[Any]):
                                data[field_name] = json.loads(data[field_name])
                            elif field_type == HttpUrl:
                                data[field_name] = HttpUrl(data[field_name])
                            elif field_type == EmailStr:
                                data[field_name] = EmailStr(data[field_name])
                            elif field_type == PhoneNumber:
                                data[field_name] = PhoneNumber(data[field_name])
                    return cls(**data)
                except Exception as e:
                    raise SparkConversionError(f"Error converting from Spark Row: {str(e)}") from e

            @classmethod
            def get_spark_schema(cls) -> StructType:
                if cls._spark_schema is None:
                    cls._spark_schema = cls._generate_spark_schema()
                return cls._spark_schema

            @classmethod
            def _generate_spark_schema(cls) -> StructType:
                schema = [
                    StructField("id", StringType(), nullable=False),
                    StructField("updated_at", TimestampType(), nullable=True),
                    StructField("metadata", MapType(StringType(), StringType()), nullable=True)
                ]

                for field_name, field in cls.__fields__.items():
                    if field_name not in ["id", "updated_at", "metadata"]:
                        if field.type_ == int:
                            schema.append(StructField(field_name, IntegerType(), nullable=field.allow_none))
                        elif field.type_ == float:
                            schema.append(StructField(field_name, FloatType(), nullable=field.allow_none))
                        elif field.type_ == bool:
                            schema.append(StructField(field_name, BooleanType(), nullable=field.allow_none))
                        elif field.type_ == str:
                            schema.append(StructField(field_name, StringType(), nullable=field.allow_none))
                        elif field.type_ == bytes:
                            schema.append(StructField(field_name, BinaryType(), nullable=field.allow_none))
                        elif field.type_ == datetime:
                            schema.append(StructField(field_name, TimestampType(), nullable=field.allow_none))
                        elif field.type_ == date:
                            schema.append(StructField(field_name, DateType(), nullable=field.allow_none))
                        else:
                            # Default to StringType for complex types
                            schema.append(StructField(field_name, StringType(), nullable=field.allow_none))

                return StructType(schema)

        return SparkWrapper
    return decorator