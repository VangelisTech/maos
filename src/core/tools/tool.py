from pydantic import BaseModel
from typing import Callable
import asyncio
import ray

from base import DomainObject


@ray.remote
def Tool(DomainObject):
    """A Base Tool Class, used by Agents to perform actions"""

    def __init__(self,
                 name: Optional[str] = Field(default="Name of the Tool", alias="name"),
                 desc: Optional[str] = Field(),
                 func: Callable = Field()
                 ):
        self.name = name
        self.desc = desc
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    async def __async_call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return f"{self.func.__name__}: {self.desc}"


# Usage
if __name__ == "__main__":
    def add(a, b):
        return a + b


    wrapped_add = Tool(func=add, description="This function adds two numbers.")