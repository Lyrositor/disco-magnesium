from dataclasses import dataclass, field

from disco_magnesium.model.actor import Actor
from disco_magnesium.model.conversation import Conversation
from disco_magnesium.model.item import Item
from disco_magnesium.model.node import Node
from disco_magnesium.model.variable import Variable


@dataclass(slots=True)
class Dialogue:
    version: str
    actors: dict[int, Actor] = field(repr=False, default_factory=dict)
    items: dict[str, Item] = field(repr=False, default_factory=dict)
    conversations: dict[int, Conversation] = field(repr=False, default_factory=dict)
    variables: dict[str, Variable] = field(repr=False, default_factory=dict)

    def get_actor(self, actor_id: int | None) -> Actor | None:
        return self.actors.get(actor_id) if actor_id else None

    def get_node(self, conversation_id: int, node_id: int) -> Node | None:
        conversation = self.conversations.get(conversation_id)
        return conversation.nodes.get(node_id) if conversation else None
