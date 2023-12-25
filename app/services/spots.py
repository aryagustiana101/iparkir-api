from datetime import datetime
from numbers import Number

from app.stripe import stripe
from app.constants import APP_URL, SPOTS_FILE_DATA
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

    increment = (file_data.get("increment") or 0) + 1

    rewrite_file_data(SPOTS_FILE_DATA, {
        "increment": increment,
        "records": [
            *(file_data.get("records") or []),
            {
                "id": increment,
                "name": name,
                "price_rate": price_rate,
                "status": status,
                "location": location,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        ],
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

    rewrite_file_data(SPOTS_FILE_DATA, {**file_data, "records": [
        {
            **spot,
            "name": name or spot["name"],
            "status": status or spot["status"],
            "location": location or spot["location"],
            "description": description or spot["description"],
            "price_rate": price_rate or spot["price_rate"],
            "updated_at": datetime.now().isoformat(),
        }
        if spot["id"] == id else
        spot
        for spot in spots
    ]})

    return {"success": True, "message": "Parking spot updated"}


def delete_spot(id: int):
    file_data = read_file_data(SPOTS_FILE_DATA)

    rewrite_file_data(SPOTS_FILE_DATA, {**file_data, "records": [
        spot for spot in (file_data.get("records") or [])
        if spot["id"] != id
    ]})

    return {"success": True, "message": "Parking spot deleted"}


def reserve_spot(spot_id: int, user_id: int):
    spot = get_spot(spot_id).get("data")

    if not spot:
        return {"success": False, "message": "Parking spot not found"}

    session = stripe.checkout.Session.create(
        mode="payment",
        cancel_url=f"{APP_URL}",
        success_url=f"{APP_URL}",
        line_items=[{
            "quantity": 1,
            "price_data": {
                "currency": "idr",
                "unit_amount": spot.get("price_rate") * 100,
                "product_data": {
                    "name": f"Reserve Parking Spot -  {spot.get('name')}",
                },
            },
        }],
    )

    return {"success": True, "redirect_url": session.url}
