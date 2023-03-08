from fastapi import APIRouter
from starlette.responses import Response

from disco_magnesium.api.app import get_dialogue
from disco_magnesium.api.difficulty import get_passive_difficulty_descriptor
from disco_magnesium.api.models.responses import ConversationResponse, InitResponse, ConversationEntry
from disco_magnesium.api.models.rolls import RollResult
from disco_magnesium.api.models.state import State
from disco_magnesium.api.reader import Reader
from disco_magnesium.model.conversation import ConversationType
from disco_magnesium.model.dialogue import Dialogue


router = APIRouter()


@router.get("/init", response_model=InitResponse)
def init(dialogue: Dialogue = get_dialogue) -> InitResponse:
    return InitResponse(
        state=State(
            variables={
                variable.name: variable.initial_value
                for variable in dialogue.variables.values()
                if variable.initial_value
            },
        ),
        variables={
            variable.name: type(variable.initial_value).__name__ for variable in dialogue.variables.values()
        },
        items=list(dialogue.items.keys()),
        conversations=[
            ConversationEntry(
                id=conversation.id,
                title=conversation.title_custom or conversation.title,
                description=conversation.description,
                type=conversation.type,
                condition=conversation.condition,
                skill=conversation.skill,
                difficulty=conversation.difficulty,
                difficulty_descriptor=get_passive_difficulty_descriptor(conversation.difficulty),
                start_node_id=conversation.start_node_id,
            )
            for conversation in dialogue.conversations.values()
            if not conversation.ignored
        ],
    )


@router.post("/conversation/{conversation_id}/choose/{option_id}", response_model=ConversationResponse)
def choose(
    state: State,
    conversation_id: int,
    option_id: int,
    roll: RollResult | None = None,
    dialogue: Dialogue = get_dialogue,
) -> Response:
    # Returning the response object directly leads to issues with the serialization of boolean variables mixed in with
    # integer variables, so we force FastAPI to bypass this process
    return Response(
        content=Reader(dialogue=dialogue, state=state).go_to_node_by_id(conversation_id, option_id, roll).json(),
        media_type="application/json"
    )
