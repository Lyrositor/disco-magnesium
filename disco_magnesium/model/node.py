from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from disco_magnesium.model.actor import Actor
from disco_magnesium.model.skill import Skill, get_skill_from_name

if TYPE_CHECKING:
    from disco_magnesium.model.conversation import Conversation


class NodeType(Enum):
    REGULAR = "Regular"
    FORK = "Fork"


@dataclass(slots=True)
class DialogueOption:
    text: str | None = None
    condition: str | None = None


@dataclass(slots=True)
class Node:
    id: int
    title: str
    type: NodeType
    is_group: bool
    conversation: "Conversation" = field(repr=False)
    actor: Actor | None = None

    skill_type: Skill | None = None
    difficulty_pass: int | None = None
    difficulty_red: int | None = None
    difficulty_white: int | None = None
    always_succeed: bool | None = None
    anti_passive: bool = False
    flag_name: str | None = None

    cost: int | None = None

    condition: str | None = None
    user_script: str | None = None
    sequence: str | None = None
    hidden: bool | None = None

    main_dialogue: str | None = None
    alternative_dialogue: list[DialogueOption] = field(repr=False, default_factory=list)
    outgoing_nodes: list[Node] = field(repr=False, default_factory=list)

    @property
    def skill(self) -> Skill | None:
        if self.skill_type:
            return self.skill_type
        elif self.actor:
            return get_skill_from_name(self.actor.short_name)
        return None

    @property
    def full_id(self) -> str:
        return f"{self.conversation.id}/{self.id}"
