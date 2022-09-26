from typing import Union

from pydantic import BaseModel


class Example(BaseModel):
    value: str  # Some relevant data
    name: Union[str, None] = "example"  # Some name
    enable_something: bool = True  # Some bool example
