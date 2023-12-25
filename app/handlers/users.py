from flask import jsonify, request

from app.services import auth


def get_current_user():
    result = auth.get_authenticated_user(request.headers.get("Authorization"))

    return jsonify(result), 200 if result.get("success") else 401
