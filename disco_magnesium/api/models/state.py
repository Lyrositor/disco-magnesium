from enum import Enum

from pydantic import BaseModel

from disco_magnesium.api.models.rolls import RollResult
from disco_magnesium.model.skill import Skill


class StoredRollResult(BaseModel):
    roll: RollResult
    difficulty_descriptor: str


class State(BaseModel):
    conversation_id: int | None = None
    node_id: int | None = None
    stored_roll: StoredRollResult | None = None
    show_all: bool = False
    show_conditions: bool = False

    money: int = 0
    day: int = 1
    time: int = 8
    damage_health: int = 0
    damage_morale: int = 0
    is_kim_here: bool = False
    is_kim_wearing_piss_jacket: bool = False  # TODO UI
    is_cuno_in_party: bool = False
    is_outside: bool = False  # TODO UI
    is_raining: bool = False
    is_snowing: bool = False
    is_hardcore: bool = False
    has_beaten_hardcore: bool = False
    items: set[str] = set()
    equipped: set[str] = set()
    variables: dict[str, int | bool] = {}
    skills: dict[str, int] = {skill.value: 3 for skill in Skill}
    thoughts: dict[str, str] = {}  # TODO UI
