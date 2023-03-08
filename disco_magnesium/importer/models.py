from dataclasses import dataclass, field
from typing import Any, Self

from disco_magnesium.importer.fields import get_fields_as_dict, get_list_from_numbered_field
from disco_magnesium.model.item import ItemGroup, ItemType
from disco_magnesium.model.skill import Skill

SOURCE_ITEM_GROUPS = {
    1: ItemGroup.ALCOHOL,
    2: ItemGroup.SMOKES,
    3: ItemGroup.GHB,
    4: ItemGroup.SPEED,
    5: ItemGroup.PYRHOLIDON,
    6: ItemGroup.TARE,
}

SOURCE_SKILLS = {
    1: Skill.LOGIC,
    2: Skill.ENCYCLOPEDIA,
    3: Skill.RHETORIC,
    4: Skill.DRAMA,
    5: Skill.CONCEPTUALIZATION,
    6: Skill.VOLITION,
    7: Skill.INLAND_EMPIRE,
    8: Skill.EMPATHY,
    9: Skill.ESPRIT_DE_CORPS,
    10: Skill.ELECTRO_CHEMISTRY,
    11: Skill.ENDURANCE,
    12: Skill.HALF_LIGHT,
    13: Skill.PAIN_THRESHOLD,
    14: Skill.SHIVERS,
    15: Skill.PERCEPTION,
    16: Skill.PERCEPTION,
    17: Skill.PERCEPTION,
    18: Skill.COMPOSURE,
    19: Skill.AUTHORITY,
    20: Skill.PHYSICAL_INSTRUMENT,
    21: Skill.INTERFACING,
    22: Skill.SUGGESTION,
    23: Skill.HAND_EYE_COORDINATION,
    24: Skill.REACTION_SPEED,
    25: Skill.SAVOIR_FAIRE,
    26: Skill.VISUAL_CALCULUS,
}

SOURCE_ITEM_TYPES = {
    2: ItemType.SHIRT,
    3: ItemType.JACKET,
    5: ItemType.PANTS,
    6: ItemType.NECK,
    7: ItemType.GLASSES,
    8: ItemType.GLOVES,
    9: ItemType.HAT,
    10: ItemType.SHOES,
    11: ItemType.HELD,
    13: ItemType.NONE,
}


@dataclass(slots=False)
class SourceData:

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError

    @classmethod
    def from_source_list(cls, data: list[dict[str, Any]]) -> list[Self]:
        return [cls.from_source(entry) for entry in data]


@dataclass(slots=False)
class SourceRgbaColor(SourceData):
    r: float
    g: float
    b: float
    a: float

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        return cls(r=float(data["r"]), g=float(data["g"]), b=float(data["b"]), a=float(data["a"]))


@dataclass(slots=False)
class SourceEmphasisSetting(SourceData):
    color: SourceRgbaColor
    bold: bool
    italic: bool
    underline: bool

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        return cls(
            color=SourceRgbaColor.from_source(data["color"]),
            bold=bool(int(data["bold"])),
            italic=bool(int(data["italic"])),
            underline=bool(int(data["underline"])),
        )


@dataclass(slots=False)
class SourceActor(SourceData):
    id: int
    name: str
    character_short_name: str
    description: str
    is_player: bool
    articy_id: str
    is_npc: bool | None = None
    is_female: bool | None = None
    short_description: str | None = None
    long_description: str | None = None
    pictures: str | None = None
    color: int | None = None

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        fields = get_fields_as_dict(data["fields"])
        return cls(
            id=data["id"],
            name=fields["Name"],
            character_short_name=fields["character_short_name"],
            description=fields["Description"],
            is_player=fields["IsPlayer"],
            articy_id=fields["Articy Id"],
            is_npc=fields.get("IsNPC"),
            is_female=fields.get("IsFemale"),
            short_description=fields.get("short_description"),
            long_description=fields.get("LongDescription"),
            pictures=fields.get("Pictures"),
            color=fields.get("color"),
        )


@dataclass(slots=False)
class SourceItem(SourceData):
    id: int
    name: str
    character_short_name: str
    description: str
    is_item: bool
    conversation: str
    articy_id: str
    is_thought: bool | None = None
    is_substance: bool | None = None
    is_consumable: bool | None = None
    cursed: bool | None = None
    auto_equip: bool | None = None
    multiple_allowed: bool | None = None
    item_type: int | None = None
    item_group: int | None = None
    item_value: int | None = None
    tooltip: str | None = None
    fixture_bonus: str | None = None
    fixture_description: str | None = None
    requirement: str | None = None
    bonus: str | None = None
    stack_name: str | None = None
    medium_text_value: str | None = None
    equip_orb: str | None = None
    alternative_equip_orb: str | None = None
    sound: int | None = None
    time_left: int | None = None
    thought_type: int | None = None

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        fields = get_fields_as_dict(data["fields"])
        return cls(
            id=data["id"],
            name=fields.get("Name"),
            character_short_name=fields["character_short_name"],
            description=fields["description"],
            is_item=fields["IsItem"],
            conversation=fields["conversation"],
            articy_id=fields["Articy Id"],
            is_thought=fields.get("isThought"),
            is_substance=fields.get("isSubstance"),
            is_consumable=fields.get("isConsumable"),
            cursed=fields.get("cursed"),
            auto_equip=fields.get("autoequip"),
            multiple_allowed=fields.get("multipleAllowed"),
            item_type=fields.get("itemType"),
            item_group=fields.get("itemGroup"),
            item_value=fields.get("itemValue"),
            tooltip=fields.get("Tooltip"),
            fixture_bonus=fields.get("fixtureBonus"),
            fixture_description=fields.get("fixtureDescription"),
            requirement=fields.get("requirement"),
            bonus=fields.get("bonus"),
            stack_name=fields.get("stackName"),
            medium_text_value=fields.get("MediumTextValue"),
            equip_orb=fields.get("equipOrb"),
            alternative_equip_orb=fields.get("alternativeEquipOrb"),
            sound=fields.get("sound"),
            time_left=fields.get("timeLeft"),
            thought_type=fields.get("thoughtType"),
        )


@dataclass(slots=False)
class SourceVariable(SourceData):
    id: int
    name: str
    initial_value: bool
    description: str | None = None

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        fields = get_fields_as_dict(data["fields"])
        return cls(
            id=data["id"],
            name=fields["Name"],
            initial_value=fields["Initial Value"],
            description=fields.get("Description"),
        )


@dataclass(slots=False)
class SourceLink(SourceData):
    origin_conversation_id: int
    origin_dialogue_id: int
    destination_conversation_id: int
    destination_dialogue_id: int
    is_connector: bool
    priority: int

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        return cls(
            origin_conversation_id=int(data["originConversationID"]),
            origin_dialogue_id=int(data["originDialogueID"]),
            destination_conversation_id=int(data["destinationConversationID"]),
            destination_dialogue_id=int(data["destinationDialogueID"]),
            is_connector=bool(int(data["isConnector"])),
            priority=int(data["priority"]),
        )


@dataclass(slots=False)
class SourceDialogueEntry(SourceData):
    id: int
    title: str
    articy_id: str
    conversation_id: int
    is_root: bool
    is_group: bool
    conditions_string: str
    user_script: str
    actor: int | None = None
    conversant: int | None = None
    color: int | None = None
    difficulty_red: int | None = None
    difficulty_white: int | None = None
    difficulty_pass: int | None = None
    click_cost: int | None = None
    dialogue_entry_type: str | None = None
    dialogue_text: str | None = None
    menu_text: str | None = None
    sequence: str | None = None
    hidden_not_enough: bool | None = None
    hidden_test: bool | None = None
    cost_once: bool | None = None
    forced: bool | None = None
    anti_passive: bool = False
    always_play_voice: bool | None = None
    play_voice_in_psychological_mode: bool | None = None
    always_succeed: bool | None = None
    flag_name: str | None = None
    check_target: str | None = None
    skill_type: str | None = None
    input_id: str | None = None
    output_id: str | None = None
    conditions: list[str] = field(default_factory=list)
    alternates: list[str] = field(default_factory=list)
    modifiers: list[int] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    tooltips: list[str] = field(default_factory=list)
    outgoing_links: list[SourceLink] = field(default_factory=list)

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        fields = get_fields_as_dict(data["fields"])
        return cls(
            id=data["id"],
            title=fields["Title"],
            articy_id=fields["Articy Id"],
            conversation_id=data["conversationID"],
            is_root=bool(int(data["isRoot"])),
            is_group=bool(int(data["isGroup"])),
            conditions_string=data["conditionsString"],
            user_script=data["userScript"],
            actor=fields.get("Actor"),
            conversant=fields.get("Conversant"),
            color=fields.get("color"),
            difficulty_red=fields.get("DifficultyRed"),
            difficulty_white=fields.get("DifficultyWhite"),
            difficulty_pass=fields.get("DifficultyPass"),
            click_cost=int(fields["ClickCost"]) if "ClickCost" in fields else None,
            dialogue_entry_type=fields.get("DialogueEntryType"),
            dialogue_text=fields.get("Dialogue Text"),
            menu_text=fields.get("Menu Text"),
            sequence=fields.get("Sequence"),
            hidden_not_enough=fields.get("HiddenNotEnough"),
            hidden_test=fields.get("HiddenTest"),
            cost_once=fields.get("CostOnce"),
            forced=fields.get("Forced"),
            anti_passive=fields.get("Antipassive") or False,
            always_play_voice=fields.get("AlwaysPlayVoice"),
            play_voice_in_psychological_mode=fields.get("PlayVoiceInPsychologicalMode"),
            always_succeed=fields.get("AlwaysSucceed"),
            flag_name=fields.get("FlagName"),
            check_target=fields.get("check_target"),
            skill_type=fields.get("SkillType"),
            input_id=fields.get("InputId"),
            output_id=fields.get("OutputId"),
            conditions=get_list_from_numbered_field(fields, "Condition", False),
            alternates=get_list_from_numbered_field(fields, "Alternate", False),
            modifiers=get_list_from_numbered_field(fields, "modifier", False),
            variables=get_list_from_numbered_field(fields, "variable", False),
            tooltips=get_list_from_numbered_field(fields, "tooltip", False),
            outgoing_links=SourceLink.from_source_list(data["outgoingLinks"]),
        )


@dataclass(slots=False)
class SourceConversation(SourceData):
    id: int
    title: str
    articy_id: str
    description: str | None = None
    alternate_orb_text: str | None = None
    actor: int | None = None
    conversant: int | None = None
    check_type: int | None = None
    condition: str | None = None
    override_dialogue_condition: str | None = None
    cancel_condition_main: str | None = None
    display_condition_main: str | None = None
    done_condition_main: str | None = None
    timed_subtasks: list[bool | None] = None
    instruction: str | None = None
    on_use: str | None = None
    orb_sound_group: str | None = None
    orb_sound_variation: str | None = None
    orb_sound_volume: int | None = None
    placement: str | None = None
    difficulty: int | None = None
    vis_cal_difficulty: int | None = None
    task_reward: int | None = None
    task_timed: bool | None = None
    cancel_subtasks: list[str] = field(default_factory=list)
    display_subtasks: list[str] = field(default_factory=list)
    done_subtasks: list[str] = field(default_factory=list)
    subtasks_title: list[str] = field(default_factory=list)
    dialogue_entries: list[SourceDialogueEntry] = field(default_factory=list)

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        fields = get_fields_as_dict(data["fields"])
        return cls(
            id=data["id"],
            title=fields["Title"],
            articy_id=fields["Articy Id"],
            description=fields.get("Description"),
            alternate_orb_text=fields.get("AlternateOrbText"),
            actor=fields.get("Actor"),
            conversant=fields.get("Conversant"),
            check_type=fields.get("CheckType"),
            condition=fields.get("Condition") or fields.get("condition"),
            override_dialogue_condition=fields.get("OverrideDialogueCondition"),
            cancel_condition_main=fields.get("cancel_condition_main"),
            display_condition_main=fields.get("display_condition_main"),
            done_condition_main=fields.get("done_condition_main"),
            instruction=fields.get("Instruction"),
            on_use=fields.get("OnUse"),
            orb_sound_group=fields.get("orbSoundGroup"),
            orb_sound_variation=fields.get("orbSoundVariation"),
            orb_sound_volume=fields.get("orbSoundVolume"),
            placement=fields.get("Placement"),
            difficulty=difficulty if (difficulty := fields.get("Difficulty")) != "" else None,
            vis_cal_difficulty=fields.get("VisCalDifficulty"),
            task_reward=fields.get("task_reward"),
            task_timed=fields.get("task_timed"),
            cancel_subtasks=get_list_from_numbered_field(fields, "cancel_subtask_", False),
            display_subtasks=get_list_from_numbered_field(fields, "display_subtask_", False),
            done_subtasks=get_list_from_numbered_field(fields, "done_subtask_", False),
            subtasks_title=get_list_from_numbered_field(fields, "subtask_title_", False),
            timed_subtasks=get_list_from_numbered_field(fields, "timed_subtask_"),
            dialogue_entries=SourceDialogueEntry.from_source_list(data["dialogueEntries"]),
        )


@dataclass(slots=False)
class SourceDialogue(SourceData):
    version: str
    author: str
    description: str
    global_user_script: str
    emphasis_settings: list[SourceEmphasisSetting]
    actors: list[SourceActor]
    items: list[SourceItem]
    variables: list[SourceVariable]
    conversations: list[SourceConversation]

    @classmethod
    def from_source(cls, data: dict[str, Any]) -> Self:
        return cls(
            version=data["version"],
            author=data["author"],
            description=data["description"],
            global_user_script=data["globalUserScript"],
            emphasis_settings=SourceEmphasisSetting.from_source_list(data["emphasisSettings"]),
            actors=SourceActor.from_source_list(data["actors"]),
            items=SourceItem.from_source_list(data["items"]),
            variables=SourceVariable.from_source_list(data["variables"]),
            conversations=SourceConversation.from_source_list(data["conversations"]),
        )
