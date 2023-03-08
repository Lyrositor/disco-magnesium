from disco_magnesium.model.node import Node

IMPOSSIBLE_DIFFICULTY = 20


def get_difficulty(node: Node) -> tuple[int | None, str | None]:
    difficulty = None

    is_active = True
    if node.difficulty_red is not None:
        difficulty = node.difficulty_red
    elif node.difficulty_white is not None:
        difficulty = node.difficulty_white
    elif node.difficulty_pass is not None:
        difficulty = node.difficulty_pass
        is_active = False

    if is_active:
        if node.always_succeed is True:
            difficulty = 0
        elif node.always_succeed is False:
            difficulty = IMPOSSIBLE_DIFFICULTY
        difficulty_descriptor = get_active_difficulty_descriptor(difficulty)
    else:
        difficulty_descriptor = get_passive_difficulty_descriptor(difficulty)

    return difficulty, difficulty_descriptor


def get_passive_difficulty_descriptor(difficulty: int | None) -> str | None:
    return get_active_difficulty_descriptor(difficulty + 6) if difficulty is not None else None


def get_active_difficulty_descriptor(difficulty: int | None) -> str | None:
    if difficulty is None:
        return None
    if difficulty >= 18:
        return "Impossible"
    elif difficulty >= 16:
        return "Godly"
    elif difficulty >= 15:
        return "Heroic"
    elif difficulty >= 14:
        return "Legendary"
    elif difficulty >= 13:
        return "Formidable"
    elif difficulty >= 12:
        return "Challenging"
    elif difficulty >= 10:
        return "Medium"
    elif difficulty >= 8:
        return "Easy"
    else:
        return "Trivial"
