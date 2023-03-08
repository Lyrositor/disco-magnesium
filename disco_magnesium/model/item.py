from dataclasses import dataclass
from enum import Enum


class ItemGroup(Enum):
    ALCOHOL = "alcohol"
    SMOKES = "smokes"
    GHB = "ghb"
    SPEED = "speed"
    PYRHOLIDON = "pyrholidon"
    TARE = "tare"


class ItemType(Enum):
    SHIRT = "shirt"
    JACKET = "jacket"
    PANTS = "pants"
    NECK = "neck"
    GLASSES = "glasses"
    GLOVES = "gloves"
    HAT = "hat"
    SHOES = "shoes"
    HELD = "held"
    NONE = "none"


@dataclass(slots=False)
class Item:
    id: int
    name: str
    group: ItemGroup | None
    type: ItemType
