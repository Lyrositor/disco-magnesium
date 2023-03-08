from enum import Enum

from pydantic import BaseModel

from disco_magnesium.api.models.state import State
from disco_magnesium.model.conversation import ConversationType
from disco_magnesium.model.skill import Skill


class MenuOptionType(Enum):
    NORMAL = "normal"
    WHITE = "white"
    RED = "red"


class ConversationEntry(BaseModel):
    id: int
    title: str
    description: str | None
    type: ConversationType
    condition: str | None = None
    skill: Skill | None = None
    difficulty: int | None = None
    difficulty_descriptor: str | None = None
    start_node_id: int = 0


class DialogueBlock(BaseModel):
    author: str | None
    color: int | None
    text: str
    skill: Skill | None = None
    difficulty_descriptor: str | None = None
    success: bool | None = None


class MenuOption(BaseModel):
    conversation_id: int
    node_id: int
    text: str
    type: MenuOptionType
    condition: str | None = None
    cost: int | None = None
    skill: Skill | None = None
    difficulty: int | None = None
    difficulty_descriptor: str | None = None


class ConversationResponse(BaseModel):
    state: State
    dialogue: list[DialogueBlock] = []
    options: list[MenuOption] = []
    continue_option: MenuOption | None = None


class InitResponse(BaseModel):
    state: State
    variables: dict[str, str] = {}
    items: list[str] = []
    conversations: list[ConversationEntry] = []
