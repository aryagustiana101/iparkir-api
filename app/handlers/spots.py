from numbers import Number
from flask import jsonify, request

from app.services import spots
from app.utils import validate_fields

schema = {
    "name": {"type": str, "failed_message": "Name is required and must be string"},
    "status": {"type": str, "failed_message": "Status is required and must be string"},
    "location": {"type": str, "failed_message": "Location is required and must be string"},
    "description": {"type": str, "failed_message": "Description is required and must be string"},
    "price_rate": {"type": Number, "failed_message": "Price rate is required and must be number"},
}


def get_spots():
    page = request.args.get("page")
    search = request.args.get("search")
    status = request.args.get("status")
    page_size = request.args.get("page_size")

    params = {
        "search": str(search) if not search is None else None,
        "status": str(status) if not status is None else None,
        "page": int(page) if (not page is None) and page.isnumeric() else 1,
        "page_size": int(page_size) if (not page_size is None) and page_size.isnumeric() else 10,
    }

    return jsonify(spots.get_spots(**params))


def get_spot(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid parking spot id"}), 400

    result = spots.get_spot(int(id))

    return jsonify(result), 200 if result.get("success") else 404


def create_spot():
    body = request.get_json()

    data = {
        "name": body.get("name"),
        "location": body.get("location"),
        "price_rate": body.get("price_rate"),
        "description": body.get("description"),
        "status": body.get("status") or "available",
    }

    validation_result = validate_fields(schema=schema, data=data)

    if not validation_result.get("success"):
        return jsonify(validation_result), 400

    result = spots.create_spot(
        name=str(data["name"]),
        status=str(data["status"]),
        price_rate=data["price_rate"],
        location=str(data["location"]),
        description=str(data["description"]),
    )

    return jsonify(result), 200 if result.get("success") else 400


def update_spot(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid parking spot id"}), 400

    spot = spots.get_spot(int(id)).get("data")

    if not spot:
        return jsonify({"success": False, "message": "Parking spot not found"}), 404

    body = request.get_json()

    data = {
        "name": body.get("name") or spot.get("name"),
        "status": body.get("status") or spot.get("status"),
        "location": body.get("location") or spot.get("location"),
        "price_rate": body.get("price_rate") or spot.get("price_rate"),
        "description": body.get("description") or spot.get("description"),
    }

    validation_result = validate_fields(schema=schema, data=data)

    if not validation_result.get("success"):
        return jsonify(validation_result), 400

    result = spots.update_spot(
        id=int(id),
        name=str(data["name"]),
        status=str(data["status"]),
        price_rate=data["price_rate"],
        location=str(data["location"]),
        description=str(data["description"]),
    )

    return jsonify(result), 200 if result.get("success") else 400


def delete_spot(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid parking spot id"}), 400

    spot = spots.get_spot(int(id)).get("data")

    if not spot:
        return jsonify({"success": False, "message": "Parking spot not found"}), 404

    result = spots.delete_spot(int(id))

    return jsonify(result), 200 if result.get("success") else 400
