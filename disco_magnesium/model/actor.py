from dataclasses import dataclass


@dataclass(slots=True)
class Actor:
    id: int
    name: str
    short_name: str
    description: str
    is_player: bool
    color: int | None = None
