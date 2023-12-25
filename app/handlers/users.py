from flask import jsonify, request

from app.services.auth import get_authenticated_user


def get_current_user():
    result = get_authenticated_user(request.headers.get("Authorization"))

    return jsonify(result), 200 if result.get("success") else 401
