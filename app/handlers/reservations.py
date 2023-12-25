from flask import jsonify, request

from app.libs.utils import validate_fields
from app.services import auth, reservations


def get_reservations():
    user = auth.get_authenticated_user(
        request.headers.get("Authorization")
    ).get("data")

    if not user:
        return jsonify({"success": False, "message":  "User not found", }), 404

    page = request.args.get("page")
    status = request.args.get("status")
    page_size = request.args.get("page_size")

    params = {
        "user_id": user.get("user_id"),
        "status": str(status) if not status is None else None,
        "is_admin_user": auth.check_admin_user(user.get("user_id")),
        "page": int(page) if (not page is None) and page.isnumeric() else 1,
        "page_size": int(page_size) if (not page_size is None) and page_size.isnumeric() else 10,
    }

    return jsonify(reservations.get_reservations(**params))


def get_reservation(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid reservation id"}), 400

    user = auth.get_authenticated_user(
        request.headers.get("Authorization")
    ).get("data")

    if not user:
        return jsonify({"success": False, "message":  "User not found", }), 404

    result = reservations.get_reservation(
        id=int(id),
        user_id=user.get("user_id"),
        is_admin_user=auth.check_admin_user(user.get("user_id"))
    )

    return jsonify(result), 200 if result.get("success") else 404


def update_reservation(id: str):
    if not id.isnumeric():
        return jsonify({"success": False, "message": "Invalid reservation id"}), 400

    user = auth.get_authenticated_user(
        request.headers.get("Authorization")
    ).get("data")

    if not user:
        return jsonify({"success": False, "message":  "User not found", }), 404

    reservation = reservations.get_reservation(
        id=int(id),
        user_id=user.get("user_id"),
        is_admin_user=auth.check_admin_user(user.get("user_id"))
    ).get("data")

    if not reservation:
        return jsonify({"success": False, "message": "Reservation not found"}), 404

    body = request.get_json()

    data = {
        "status": body.get("status"),
        "id": int(reservation.get("id")),
    }

    validation_result = validate_fields(data=data, schema={
        "status": {"type": str, "failed_message": "Status is required and must be string"},
        "id": {"type": int, "failed_message": "Reservation ID is required and must number"},
    })

    if not validation_result.get("success"):
        return jsonify(validation_result), 400

    result = reservations.update_reservation(**data)

    return jsonify(result), 200 if result.get("success") else 400
