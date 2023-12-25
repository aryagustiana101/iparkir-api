from numbers import Number
from datetime import datetime
from flask import jsonify, request

from app.services import auth, spots
from app.utils import parse_iso_datetime, validate_fields

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


def reserve_spot(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid parking spot id"}), 400

    user = auth.get_authenticated_user(
        request.headers.get("Authorization")
    ).get("data")

    spot = spots.get_spot(int(id)).get("data")

    if not spot or not user:
        return jsonify({
            "success": False,
            "message":  "Parking spot not found" if not spot else "User not found",
        }), 404

    if spot.get("status") != "available":
        return jsonify({"success": False, "message":  "Parking spot is not available"}), 400

    body = request.get_json()

    data = {
        "spot_id": int(id),
        "user_id": user.get("user_id"),
        "end": parse_iso_datetime(body.get("end")),
        "start": parse_iso_datetime(body.get("start")),
    }

    validation_result = validate_fields(data=data, schema={
        "user_id": {"type": str, "failed_message": "User ID is required and must be string"},
        "spot_id": {"type": int, "failed_message": "Spot ID is required and must be number"},
        "end": {
            "type": datetime,
            "failed_message": "End date time is required and must be date with ISO format"
        },
        "start": {
            "type": datetime,
            "failed_message": "Start date time is required and must be date with ISO format"
        },
    })

    if not validation_result.get("success"):
        return jsonify(validation_result), 400

    if data["end"] <= data["start"]:
        return jsonify(
            {"success": False, "message": "End date time must be greater than start date time"}
        )

    current_time = datetime.now()

    if data["start"] < current_time or data["end"] < current_time:
        return {
            "success": False,
            "message":
                "Start date time must not be in the past"
                if data["start"] < current_time else
                "End date time must not be in the past",
        }

    result = spots.reserve_spot(**data)

    return result, 200 if result.get("success") else 400
