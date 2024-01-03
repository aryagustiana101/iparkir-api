import os
import json
from datetime import datetime
from typing import Any, Callable

from app.libs.constants import DEFAULT_FILE_DATA_FORMAT


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
                rules.get("failed_message") or f"Invalid field {field}"
            )

    result["success"] = len(result["messages"]) == 0

    return result


def binary_search(data: list[Any], search: Any, key_function: Callable = lambda x: x):
    sorted_data = bubble_sort(data, key_function)

    left = 0
    right = len(sorted_data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_key = key_function(sorted_data[mid])

        if mid_key == search:
            return sorted_data[mid]

        if mid_key < search:
            left = mid + 1
        else:
            right = mid - 1

    return None


def parse_iso_datetime(value: str):
    try:
        return datetime.fromisoformat(value)
    except Exception as e:
        print(e)
        return None


def bubble_sort(data: list[Any], key_function: Callable = lambda x: x):
    n = len(data)

    for i in range(n):
        is_sorted = True

        for j in range(n - i - 1):
            if key_function(data[j]) > key_function(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
                is_sorted = False

        if is_sorted:
            break

    return data
