from typing import Any


def get_fields_as_dict(fields_list: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        field["title"]: convert_field_value(field["value"], field["type"])
        for field in fields_list
    }


def get_list_from_numbered_field(
    fields_dict: dict[str, Any], field_prefix: str, include_empty: bool = True
) -> list[Any]:
    return [
        fields_dict[field_name]
        for field_name in sorted(
            (field_name for field_name in fields_dict if field_name.startswith(field_prefix)),
            key=lambda field_name: int(field_name[len(field_prefix):])
        )
        if include_empty or fields_dict[field_name] not in ("", None)
    ]


def convert_field_value(value: str, field_type: int) -> str | int | bool | None:
    match field_type:
        case 0:
            return value
        case 1 | 5:
            return int(value) if value.strip() else None
        case 2:
            match value:
                case "True":
                    return True
                case "False":
                    return False
                case "":
                    return None
                case _:
                    raise ValueError(f"Unexpected boolean value: {value}")
        case _:
            raise ValueError(f"Unexpected field type: {field_type}")
