from datetime import datetime
from typing import Any

from app.libs.constants import RESERVATIONS_FILE_DATA
from app.libs.utils import binary_search, read_file_data, rewrite_file_data


def get_reservations(
    user_id: str,
    page: int = 1,
    page_size: int = 10,
    status: str | None = None,
    is_admin_user: bool = False
):
    file_data = read_file_data(RESERVATIONS_FILE_DATA)

    reservations = file_data.get("records") or []

    filtered_reservations = \
        reservations if is_admin_user else \
        list(filter(
            lambda x: x["user"]["user_id"] == user_id, reservations
        ))

    filtered_reservations = \
        filtered_reservations if not status else \
        list(filter(lambda x: x["status"] == status, filtered_reservations))

    start = (page - 1) * page_size
    end = start + page_size

    paginated_reservations = filtered_reservations[start:end]

    return {
        "success": True,
        "metadata": {
            "page": page,
            "page_size": page_size,
            "total": len(filtered_reservations),
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": len(filtered_reservations) // page_size,
            "next_page": page + 1 if page < len(filtered_reservations) // page_size + 1 else None,
        },
        "data": paginated_reservations
    }


def get_reservation(id: int, user_id: str, is_admin_user: bool = False):
    file_data = read_file_data(RESERVATIONS_FILE_DATA)

    reservation = binary_search(
        search=id,
        key_function=lambda x: x["id"],
        data=file_data.get("records") or [],
    )

    success = \
        reservation is not None and \
        (is_admin_user or reservation["user"]["user_id"] == user_id)

    result = {"success": success}

    return \
        {**result, "message": "Reservation not found"} if not success else \
        {**result, "data": reservation}


def create_reservation(data: dict[str, Any]):
    file_data = read_file_data(RESERVATIONS_FILE_DATA)

    increment = (file_data.get("increment") or 0) + 1

    reservation = {
        **data,
        "id": increment,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    rewrite_file_data(RESERVATIONS_FILE_DATA, {
        "increment": increment,
        "records": [*(file_data.get("records") or []), reservation],
    })

    return {"success": True, "message": "Reservation created", "data": reservation}


def update_reservation(id: int, status: str):
    file_data = read_file_data(RESERVATIONS_FILE_DATA)

    reservations = file_data.get("records") or []

    rewrite_file_data(RESERVATIONS_FILE_DATA, {
        **file_data,
        "records": [
            {
                **reservation,
                "status": status,
                "updated_at": datetime.now().isoformat(),
            }
            if reservation["id"] == id else
            reservation
            for reservation in reservations
        ],
    })

    return {"success": True, "message": "Reservation updated"}
