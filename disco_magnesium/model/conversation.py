from dataclasses import dataclass, field
from enum import Enum

from disco_magnesium.model.actor import Actor
from disco_magnesium.model.node import Node
from disco_magnesium.model.skill import Skill


class ConversationType(Enum):
    EXCHANGE = "exchange"
    THOUGHT = "thought"
    ORB = "orb"
    BARK = "bark"
    TASK = "task"


@dataclass(slots=True)
class Conversation:
    id: int
    title: str
    description: str | None = None
    actor: Actor | None = None
    conversant: Actor | None = None
    condition: str | None = None
    skill: Skill | None = None
    difficulty: int | None = None
    instruction: str | None = None
    nodes: dict[int, Node] = field(repr=False, default_factory=dict)

    # Metadata
    title_custom: str | None = None
    start_node_id: int = 0
    type: ConversationType = ConversationType.EXCHANGE
    ignored: bool = False
