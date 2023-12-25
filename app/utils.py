import os
import json
from typing import Any, Callable

DEFAULT_FILE_DATA_FORMAT = {
    "increment": 0,
    "records": []
}


def create_file_data(path: str, data: dict[str, Any] = DEFAULT_FILE_DATA_FORMAT):
    with open(path, "w") as file:
        return json.dump(data, file)


def read_file_data(path: str, default_data: dict[str, Any] = DEFAULT_FILE_DATA_FORMAT):
    if not os.path.exists(path):
        create_file_data(path, default_data)

    with open(path, "r") as file:
        return json.load(file)


def rewrite_file_data(path: str, data: dict[str, Any]):
    with open(path, "w") as file:
        json.dump(data, file)


def validate_field(data: Any, type: Any, required: bool | None = True):
    return not required if data is None else isinstance(data, type)


def validate_fields(data: dict[str, Any], schema: dict[str, dict[str, Any]]):
    result = {"success": False, "messages": []}

    for field, rules in schema.items():
        required = rules.get("required")

        if not validate_field(
            type=rules["type"],
            data=data.get(field),
            required=required if not required is None else True
        ):
            result["messages"].append(
                rules.get("message") or f"Invalid field {field}"
            )

    result["success"] = len(result["messages"]) == 0

    return result


def binary_search(data: list[Any], search: Any, key_function: Callable = lambda x: x):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_key = key_function(data[mid])

        if mid_key == search:
            return data[mid]

        if mid_key < search:
            left = mid + 1
        else:
            right = mid - 1

    return None