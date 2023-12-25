from datetime import datetime
from numbers import Number

from app.constants import SPOTS_FILE_DATA
from app.utils import binary_search, read_file_data, rewrite_file_data


def get_spots(search: str | None = None, page: int = 1, page_size: int = 10, status: str | None = None):
    file_data = read_file_data(SPOTS_FILE_DATA)

    spots = file_data.get("records") or []

    filtered_spots = \
        spots if not search else \
        list(filter(
            lambda x: (
                search.lower() in x["name"].lower() or
                search.lower() in x["location"].lower()
            ),
            spots
        ))

    filtered_spots = \
        filtered_spots if not status else \
        list(filter(lambda x: x["status"] == status, filtered_spots))

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_spots = filtered_spots[start_index:end_index]

    return {
        "success": True,
        "metadata": {
            "page": page,
            "page_size": page_size,
            "total": len(filtered_spots),
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": len(filtered_spots) // page_size,
            "next_page": page + 1 if page < len(filtered_spots) // page_size + 1 else None,
        },
        "data": paginated_spots
    }


def get_spot(id: int):
    file_data = read_file_data(SPOTS_FILE_DATA)

    spot = binary_search(
        search=id,
        key_function=lambda x: x["id"],
        data=file_data.get("records") or [],
    )

    result = {"success": spot is not None}

    return \
        {**result, "message": "Parking spot not found"} if not result["success"] else \
        {**result, "data": spot}


def create_spot(name: str, location: str, description: str, price_rate: Number, status: str):
    file_data = read_file_data(SPOTS_FILE_DATA)

    spots = file_data.get("records") or []
    increment = file_data.get("increment") or 0

    spots.append({
        "id": increment + 1,
        "name": name,
        "price_rate": price_rate,
        "status": status,
        "location": location,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    })

    rewrite_file_data(SPOTS_FILE_DATA, {
        "increment": increment + 1,
        "records": spots,
    })

    return {"success": True, "message": "Parking spot created"}


def update_spot(
    id: int,
    name: str | None,
    status: str | None,
    location: str | None,
    description: str | None,
    price_rate: Number | None,
):
    file_data = read_file_data(SPOTS_FILE_DATA)

    spots = file_data.get("records") or []

    for spot in spots:
        if spot["id"] == id:
            spot["name"] = name or spot["name"]
            spot["location"] = location or spot["location"]
            spot["description"] = description or spot["description"]
            spot["price_rate"] = price_rate or spot["price_rate"]
            spot["status"] = status or spot["status"]
            spot["updated_at"] = datetime.now().isoformat()

            break

    rewrite_file_data(SPOTS_FILE_DATA, {**file_data, "records": spots})

    return {"success": True, "message": "Parking spot updated"}


def delete_spot(id: int):
    file_data = read_file_data(SPOTS_FILE_DATA)

    spots = file_data.get("records") or []

    for spot in spots:
        if spot["id"] == id:
            spots.remove(spot)

            break

    rewrite_file_data(SPOTS_FILE_DATA, {**file_data, "records": spots})

    return {"success": True, "message": "Parking spot deleted"}
