import logging
from typing import Any

import orjson

from disco_magnesium.importer.models import (
    SourceDialogue,
    SourceDialogueEntry,
    SOURCE_SKILLS,
    SOURCE_ITEM_GROUPS,
    SOURCE_ITEM_TYPES,
)
from disco_magnesium.model.actor import Actor
from disco_magnesium.model.conversation import Conversation, ConversationType
from disco_magnesium.model.dialogue import Dialogue
from disco_magnesium.model.item import Item, ItemType
from disco_magnesium.model.node import Node, NodeType, DialogueOption
from disco_magnesium.model.skill import get_skill_from_name
from disco_magnesium.model.variable import Variable

log = logging.getLogger(__name__)


def import_dialogue_from_raw_json_file(json_file_path: str) -> SourceDialogue:
    log.info(f"Importing source dialogue from JSON file at: {json_file_path}")
    with open(json_file_path, encoding="utf-8") as f:
        return SourceDialogue.from_source(orjson.loads(f.read()))


def convert_source_dialogue(
    source_dialogue: SourceDialogue,
    additional_variables: dict[str, int | bool],
    conversations_metadata: dict[int, dict[str, Any]]
) -> Dialogue:
    log.info("Converting source dialogue")

    dialogue = Dialogue(version=source_dialogue.version)
    actors_by_articy_id = {}

    for source_actor in source_dialogue.actors:
        actor = Actor(
            id=source_actor.id,
            name=source_actor.name,
            short_name=source_actor.character_short_name,
            description=source_actor.description,
            is_player=source_actor.is_player,
            color=source_actor.color,
        )
        dialogue.actors[actor.id] = actor
        actors_by_articy_id[source_actor.articy_id] = actor

    for source_variable in source_dialogue.variables:
        variable = Variable(
            id=source_variable.id,
            name=source_variable.name,
            description=source_variable.description,
            initial_value=source_variable.initial_value
        )
        dialogue.variables[variable.name] = variable

    highest_variable_id = max(var.id for var in dialogue.variables.values())
    for variable_name, initial_value in additional_variables.items():
        if variable_name in dialogue.variables:
            dialogue.variables[variable_name].initial_value = initial_value
        else:
            highest_variable_id += 1
            variable = Variable(id=highest_variable_id, name=variable_name, description="", initial_value=initial_value)
            dialogue.variables[variable.name] = variable

    for source_item in source_dialogue.items:
        item = Item(
            id=source_item.id,
            name=source_item.name,
            group=SOURCE_ITEM_GROUPS[source_item.item_group] if source_item.item_group else None,
            type=SOURCE_ITEM_TYPES[source_item.item_type] if source_item.item_type else ItemType.NONE,
        )
        dialogue.items[item.name] = item

    for source_conversation in source_dialogue.conversations:
        conversation_metadata = conversations_metadata.get(source_conversation.id, {})
        default_type = ConversationType.EXCHANGE.value
        if (
            source_conversation.display_condition_main is not None
            or source_conversation.done_condition_main is not None
            or source_conversation.cancel_condition_main is not None
        ):
            default_type = ConversationType.TASK.value
        conversation = Conversation(
            id=source_conversation.id,
            title=source_conversation.title,
            description=source_conversation.description,
            actor=dialogue.actors.get(source_conversation.actor),
            conversant=dialogue.actors.get(source_conversation.conversant),
            condition=source_conversation.condition,
            skill=SOURCE_SKILLS.get(source_conversation.check_type, None),
            difficulty=int(source_conversation.difficulty) if source_conversation.difficulty is not None else None,
            instruction=source_conversation.instruction,
            title_custom=conversation_metadata.get("title"),
            start_node_id=conversation_metadata.get("start_node_id", 0),
            type=ConversationType(conversation_metadata.get("type", default_type)),
            ignored=conversation_metadata.get("ignored", False),
        )
        dialogue.conversations[conversation.id] = conversation

    outgoing_node_ids = {}
    for source_conversation in source_dialogue.conversations:
        conversation = dialogue.conversations[source_conversation.id]
        for source_dialogue_entry in source_conversation.dialogue_entries:
            node = Node(
                id=source_dialogue_entry.id,
                title=source_dialogue_entry.title,
                type=(
                    NodeType(source_dialogue_entry.dialogue_entry_type)
                    if source_dialogue_entry.dialogue_entry_type
                    else NodeType.REGULAR
                ),
                is_group=source_dialogue_entry.is_group,
                conversation=conversation,
                actor=dialogue.actors.get(source_dialogue_entry.actor),
                skill_type=(
                    get_skill_from_name(actors_by_articy_id[source_dialogue_entry.skill_type].short_name)
                    if source_dialogue_entry.skill_type else None
                ),
                difficulty_pass=source_dialogue_entry.difficulty_pass,
                difficulty_red=source_dialogue_entry.difficulty_red,
                difficulty_white=source_dialogue_entry.difficulty_white,
                always_succeed=source_dialogue_entry.always_succeed,
                anti_passive=source_dialogue_entry.anti_passive,
                flag_name=source_dialogue_entry.flag_name or None,
                cost=source_dialogue_entry.click_cost or None,
                condition=source_dialogue_entry.conditions_string or None,
                user_script=source_dialogue_entry.user_script or None,
                sequence=source_dialogue_entry.sequence or None,
                hidden=source_dialogue_entry.hidden_test,
                main_dialogue=source_dialogue_entry.dialogue_text or None,
                alternative_dialogue=_build_dialogue_options(source_dialogue_entry),
            )
            outgoing_node_ids[(conversation.id, node.id)] = [
                (link.destination_conversation_id, link.destination_dialogue_id)
                for link in source_dialogue_entry.outgoing_links
            ]
            conversation.nodes[node.id] = node

    for conversation in dialogue.conversations.values():
        for node in conversation.nodes.values():
            for outgoing_conversation_id, outgoing_node_id in outgoing_node_ids.get((conversation.id, node.id), []):
                node.outgoing_nodes.append(dialogue.conversations[outgoing_conversation_id].nodes[outgoing_node_id])

    log.info("Dialogue was successfully imported")

    return dialogue


def _build_dialogue_options(source_dialogue_entry: SourceDialogueEntry) -> list[DialogueOption]:
    return [
        DialogueOption(text=text or None, condition=condition or None)
        for text, condition in zip(source_dialogue_entry.alternates, source_dialogue_entry.conditions)
        if text or condition
    ]
