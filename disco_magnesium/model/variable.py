from dataclasses import dataclass


@dataclass(slots=False)
class Variable:
    id: int
    name: str
    description: str
    initial_value: int | bool
