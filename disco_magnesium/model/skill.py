from enum import Enum


class Skill(Enum):
    LOGIC = "logic"
    ENCYCLOPEDIA = "encyclopedia"
    RHETORIC = "rhetoric"
    DRAMA = "drama"
    CONCEPTUALIZATION = "conceptualization"
    VISUAL_CALCULUS = "visualcalculus"

    VOLITION = "volition"
    INLAND_EMPIRE = "inlandempire"
    EMPATHY = "empathy"
    AUTHORITY = "authority"
    ESPRIT_DE_CORPS = "espritdecorps"
    SUGGESTION = "suggestion"

    ENDURANCE = "endurance"
    PAIN_THRESHOLD = "painthreshold"
    PHYSICAL_INSTRUMENT = "physicalinstrument"
    ELECTRO_CHEMISTRY = "electrochemistry"
    SHIVERS = "shivers"
    HALF_LIGHT = "halflight"

    HAND_EYE_COORDINATION = "handeyecoordination"
    PERCEPTION = "perception"
    REACTION_SPEED = "reactionspeed"
    SAVOIR_FAIRE = "savoirfaire"
    INTERFACING = "interfacing"
    COMPOSURE = "composure"


SKILL_VALUES = {s.value: s for s in Skill}


def get_skill_from_name(skill_name: str) -> Skill | None:
    # Special case for perception, which is split by senses
    if skill_name.startswith("perception"):
        skill_name = "perception"
    return SKILL_VALUES.get(skill_name)
