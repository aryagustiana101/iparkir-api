from datetime import datetime
from typing import Any
from app.libs.constants import USERS_FILE_DATA
from app.libs.utils import binary_search, read_file_data, rewrite_file_data


def get_user(id: str):
    file_data = read_file_data(USERS_FILE_DATA)

    user = binary_search(
        search=id,
        key_function=lambda x: x["user_id"],
        data=file_data.get("records") or [],
    )

    result = {"success": user is not None}

    return \
        {**result, "message": "User not found"} if not result["success"] else \
        {**result, "data": user}


def create_user(data: dict[str, Any]):
    file_data = read_file_data(USERS_FILE_DATA)

    increment = (file_data.get("increment") or 0) + 1

    rewrite_file_data(USERS_FILE_DATA, {
        "increment": increment,
        "records": [
            *(file_data.get("records") or []),
            {
                **data,
                "id": increment,
                "user_id": data["id"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        ],
    })

    return {"success": True, "message": "User created"}


def update_user(id: int, data: dict[str, Any]):
    file_data = read_file_data(USERS_FILE_DATA)

    users = file_data.get("records") or []

    rewrite_file_data(USERS_FILE_DATA, {**file_data,  "records": [
        {
            **data,
            "id": user["id"],
            "user_id": data["id"],
            "created_at": user["created_at"],
            "updated_at": datetime.now().isoformat(),
        }
        if user["user_id"] == id else
        user
        for user in users
    ], })

    return {"success": True, "message": "User updated"}
