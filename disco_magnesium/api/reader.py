import logging
from collections.abc import Sequence
from enum import Enum
from typing import Iterator, Iterable

from pydantic import BaseModel

from disco_magnesium.api.difficulty import get_difficulty
from disco_magnesium.api.models.responses import ConversationResponse, DialogueBlock, MenuOption, MenuOptionType
from disco_magnesium.api.models.rolls import RollResult
from disco_magnesium.api.models.state import State, StoredRollResult
from disco_magnesium.api.script_engine import ScriptEngine
from disco_magnesium.model.conversation import ConversationType
from disco_magnesium.model.dialogue import Dialogue
from disco_magnesium.model.node import Node

log = logging.getLogger(__name__)


class ReaderException(Exception):
    pass


class Instruction(Enum):
    CONTINUE = "continue"
    SHOW_CONTINUE = "show_continue"
    SHOW_OPTIONS = "show_options"
    END = "end"


class NodeRunResult(BaseModel):
    instruction: Instruction
    dialogue: list[DialogueBlock] = []
    options: list[MenuOption] = []


class Reader:
    dialogue: Dialogue
    state: State
    script_engine: ScriptEngine
    waiting_for_input: bool

    def __init__(self, dialogue: Dialogue, state: State):
        self.dialogue = dialogue
        self.state = state
        self.script_engine = ScriptEngine(dialogue, state)
        self.waiting_for_input = False

    def go_to_node_by_id(self, conversation_id: int, node_id: int, roll: RollResult | None) -> ConversationResponse:
        self.waiting_for_input = False
        if node := self.dialogue.get_node(conversation_id, node_id):
            self.state.conversation_id = conversation_id
            self.state.node_id = node.id
            if roll is not None:
                self._apply_roll(node, roll)
            return self._run()
        raise ReaderException(f"Failed to go to node #{node_id} in conversation #{conversation_id}")

    def _apply_roll(self, node: Node, roll: RollResult) -> None:
        if node.flag_name:
            self.state.variables[node.flag_name] = roll == RollResult.SUCCESS
            difficulty, difficulty_descriptor = get_difficulty(node)
            if difficulty_descriptor:
                self.state.stored_roll = StoredRollResult(roll=roll, difficulty_descriptor=difficulty_descriptor)
            else:
                log.error(f"Missing difficulty data for node #{node.full_id}")

    def _run(self) -> ConversationResponse:
        response = ConversationResponse(state=self.state)

        while result := self._run_for_current_node():
            response.dialogue.extend(result.dialogue)
            match result.instruction:
                case Instruction.CONTINUE:
                    if result.options:
                        raise RuntimeError("Instructed to continue, but instruction has too many options")
                case Instruction.SHOW_CONTINUE:
                    response.continue_option = result.options[0]
                    break
                case Instruction.SHOW_OPTIONS:
                    response.options.extend(result.options)
                    break
                case Instruction.END:
                    if result.options:
                        raise RuntimeError("Instructed to end, but instruction has options")
                    break

        return response

    def _run_for_current_node(self) -> NodeRunResult | None:
        if not (node := self.dialogue.get_node(self.state.conversation_id, self.state.node_id)):
            return None

        if node.id == 0 and node.conversation.instruction:
            self.script_engine.run_user_script(node.conversation.instruction)

        if self._passes_passive_check(node) and node.user_script:
            self.script_engine.run_user_script(node.user_script)

        result = NodeRunResult(instruction=Instruction.CONTINUE)
        if node.conversation.type == ConversationType.ORB:
            conversation = node.conversation
            result.dialogue.append(
                DialogueBlock(
                    author=conversation.actor.name if conversation.actor else None,
                    color=conversation.actor.color if conversation.actor else None,
                    text=conversation.description or "",
                )
            )
            result.instruction = Instruction.END
            return result
        elif self._should_display_dialogue(node):
            difficulty_descriptor = None
            success = None
            if self.state.stored_roll and not _is_from_player(node):
                # Show the roll result on the first message that isn't from the player (should be from the same skill
                # that was tested)
                difficulty_descriptor = self.state.stored_roll.difficulty_descriptor
                success = self.state.stored_roll.roll == RollResult.SUCCESS
                self.state.stored_roll = None
            elif node.difficulty_pass is not None:
                difficulty_descriptor = get_difficulty(node)[1]
                success = node.anti_passive ^ self._passes_passive_check(node)

            result.dialogue.append(
                DialogueBlock(
                    author=node.actor.name if node.actor else None,
                    color=node.actor.color if node.actor else None,
                    text=self._get_node_dialogue(node),
                    skill=node.skill,
                    difficulty_descriptor=difficulty_descriptor,
                    success=success,
                )
            )
            if not _is_from_player(node):
                self.waiting_for_input = True

        eligible_outgoing_nodes = list(self._get_eligible_outgoing_nodes(node))

        if not eligible_outgoing_nodes:
            result.instruction = Instruction.END
        elif self._has_menu(eligible_outgoing_nodes):
            result.options = self._build_menu_options(eligible_outgoing_nodes)
            result.instruction = Instruction.SHOW_OPTIONS
        elif next_node := self._choose_next_node(eligible_outgoing_nodes):
            result.instruction = Instruction.CONTINUE
            self.state.conversation_id = next_node.conversation.id
            self.state.node_id = next_node.id
        else:
            result.options = self._build_menu_options(eligible_outgoing_nodes)
            result.instruction = Instruction.SHOW_CONTINUE
            result.options[0].text = "Continue"

        return result

    def _get_eligible_outgoing_nodes(self, node: Node) -> Iterator[Node]:
        """Gets all outgoing nodes whose condition is met by the current state of the game."""
        for outgoing_node in node.outgoing_nodes:
            if (
                self.state.show_all
                or not outgoing_node.condition
                or self.script_engine.eval_condition(outgoing_node.condition)
            ):
                yield outgoing_node

    def _choose_next_node(self, outgoing_nodes: Sequence[Node]) -> Node | None:
        """Chooses the next node to automatically continue to, if any.

        So long as there is no additional dialogue to display, we should keep going with the first eligible outgoing
        node.
        """
        # Pick the first eligible candidate if the choice isn't up to the player
        next_node = outgoing_nodes[0]
        if len(outgoing_nodes) > 1:
            log.error(f"Encountered multiple outgoing nodes: {outgoing_nodes}")

        # Keep going until another node wants to display dialogue, then wait
        if self._should_display_dialogue(next_node) and self.waiting_for_input:
            return None

        return next_node

    def _has_menu(self, outgoing_nodes: Sequence[Node]) -> bool:
        """Determines whether a menu is up next.

        Any branching node with at least one player option is considered a menu. This is not fully faithful to the
        in-game system, as there are a few cases where player options are mixed in with non-player options, but dealing
        with those cases is currently out of scope.

        If show_all is enabled, any branching path is shown, even if there are no player options in it.
        """
        return (
            any(self._resolve_menu_node_text(n) for n in outgoing_nodes)
            or (self.state.show_all and len(outgoing_nodes) > 1)
        )

    def _build_menu_options(self, outgoing_nodes: Iterable[Node]) -> list[MenuOption]:
        options = []
        for outgoing_node in outgoing_nodes:
            if outgoing_node.hidden and not self.state.show_all:
                continue

            if outgoing_node.difficulty_red is not None:
                option_type = MenuOptionType.RED
            elif outgoing_node.difficulty_white is not None:
                option_type = MenuOptionType.WHITE
            else:
                option_type = MenuOptionType.NORMAL

            difficulty, difficulty_descriptor = get_difficulty(outgoing_node)

            if outgoing_node.hidden:
                text = "[[hidden]]"
            elif calculated_text := self._resolve_menu_node_text(outgoing_node):
                text = calculated_text
            else:
                text = "[[no text]]"
            options.append(
                MenuOption(
                    conversation_id=outgoing_node.conversation.id,
                    node_id=outgoing_node.id,
                    text=text,
                    type=option_type,
                    condition=outgoing_node.condition,
                    cost=outgoing_node.cost,
                    skill=outgoing_node.skill,
                    difficulty=difficulty,
                    difficulty_descriptor=difficulty_descriptor,
                )
            )
        return options

    def _should_display_dialogue(self, node: Node) -> bool:
        return (node.main_dialogue or node.alternative_dialogue) and self._passes_passive_check(node)

    def _resolve_menu_node_text(self, node: Node) -> str | None:
        """Attempts to resolve an outgoing node to possible menu text.

        For most menu entries, the menu text is the text of the first outgoing node, but there are a few menus which
        make things more complicated by requiring us to follow outgoing nodes of outgoing nodes.

        This function attempts to determine the menu entry text that should be displayed, but it is not overly thorough
        about it - there are some edge-cases that it doesn't account for.

        If no menu text can be found, None is returned.
        """
        # Special case for orb Easter eggs
        if node.conversation.type == ConversationType.ORB:
            return node.conversation.description

        text = self._get_node_dialogue(node)
        if _is_from_player(node):
            return text

        if not text and len(node.outgoing_nodes) == 1:
            # Don't evaluate conditions here for simplicity's sake (this might be wrong)
            return self._resolve_menu_node_text(node.outgoing_nodes[0])
        return None

    def _passes_passive_check(self, node: Node) -> bool:
        if node.difficulty_pass and not self.state.show_all:
            skill_level = self.state.skills[node.skill.value]  # type: ignore
            if node.anti_passive:
                return skill_level < node.difficulty_pass
            else:
                return skill_level >= node.difficulty_pass
        return True

    def _get_node_dialogue(self, node: Node) -> str | None:
        if self.state.show_all:
            dialogue = []
            for alternative_dialogue in node.alternative_dialogue:
                dialogue.append(alternative_dialogue.text)
            if node.main_dialogue:
                dialogue.append(node.main_dialogue)
            return " // ".join(dialogue)
        else:
            for alternative_dialogue in node.alternative_dialogue:
                if (
                    not alternative_dialogue.condition
                    or self.script_engine.eval_condition(alternative_dialogue.condition)
                ):
                    return alternative_dialogue.text
            return node.main_dialogue


def _is_from_player(node: Node) -> bool:
    return bool(node.actor and node.actor.is_player)
