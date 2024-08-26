import json
import uuid
from datetime import datetime, date, time
from typing import Any, Dict

import pyarrow as pa
import ulid
from pydantic import HttpUrl, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ArrowConversionError(CustomModelError):
    """Raised when conversion to/from Arrow fails."""

def with_arrow(cls):
    """
    Add Arrow serialization to CustomModel subclass.
    ┌─────────────────────────────────────────────┐
    │ Methods:                                    │
    │  to_arrow()     │ Instance → Arrow table    │
    │  from_arrow()   │ Arrow table → Instance    │
    ├─────────────────────────────────────────────┤
    │ Usage: @with_arrow                          │
    │        class MyModel(CustomModel): ...      │
    ├─────────────────────────────────────────────┤
    │ Notes: • Arrow ecosystem compatible         │
    │        • Efficient in-data                │
    │        • Handle ArrowConversionError        │
    └─────────────────────────────────────────────┘
    """
    @functools.wraps(cls)
    class ArrowWrapper(cls):
        @staticmethod
        def _get_arrow_type(python_type):
            type_mapping = {
                int: pa.int64(),
                float: pa.float64(),
                bool: pa.bool_(),
                str: pa.string(),
                bytes: pa.binary(),
                datetime: pa.timestamp('ms'),
                date: pa.date32(),
                time: pa.time64('us'),
                Dict[str, Any]: pa.map_(pa.string(), pa.string()),
                List[Any]: pa.list_(pa.string()),
                uuid.UUID: pa.string(),
                ulid.ULID: pa.string(),
                HttpUrl: pa.string(),
                EmailStr: pa.string(),
                PhoneNumber: pa.string(),
            }
            return type_mapping.get(python_type, pa.string())

        def to_arrow(self) -> pa.Table:
            try:
                data = self.dict()
                fields = []
                arrays = []

                for field_name, field_value in data.items():
                    python_type = type(field_value) if field_value is not None else type(None)
                    arrow_type = self._get_arrow_type(python_type)
                    
                    fields.append(pa.field(field_name, arrow_type))
                    
                    if isinstance(field_value, (dict, list)):
                        arrays.append(pa.array([json.dumps(field_value)]))
                    elif isinstance(field_value, (datetime, date, time, uuid.UUID, ulid.ULID, HttpUrl, EmailStr, PhoneNumber)):
                        arrays.append(pa.array([str(field_value)]))
                    else:
                        arrays.append(pa.array([field_value]))

                return pa.Table.from_arrays(arrays, schema=pa.schema(fields))
            except Exception as e:
                raise ArrowConversionError(f"Error converting to Arrow: {str(e)}") from e

        @classmethod
        def from_arrow(cls, table: pa.Table) -> 'CustomModel':
            try:
                data = table.to_pydict()
                for field_name, field_type in cls.__annotations__.items():
                    if field_name in data:
                        if field_type == datetime:
                            data[field_name] = datetime.fromisoformat(data[field_name][0])
                        elif field_type == date:
                            data[field_name] = date.fromisoformat(data[field_name][0])
                        elif field_type == time:
                            data[field_name] = time.fromisoformat(data[field_name][0])
                        elif field_type in (Dict[str, Any], List[Any]):
                            data[field_name] = json.loads(data[field_name][0])
                        elif field_type == HttpUrl:
                            data[field_name] = HttpUrl(data[field_name][0])
                        elif field_type == EmailStr:
                            data[field_name] = EmailStr(data[field_name][0])
                        elif field_type == PhoneNumber:
                            data[field_name] = PhoneNumber(data[field_name][0])
                return cls(**data)
            except Exception as e:
                raise ArrowConversionError(f"Error converting from Arrow: {str(e)}") from e

    return ArrowWrapper

