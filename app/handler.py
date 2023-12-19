import app.auth as auth
import app.user as user
from flask import jsonify, request


def index():
    return jsonify({"success": True, "message": "Hello world!"})


def unsupported(_):
    return jsonify({"success": False, "message": "Unsupported request"}), 400


def google_auth():
    return jsonify(auth.google_auth())


def google_auth_callback():
    result = auth.google_auth_callback(f"{request.args.get("code")}")

    return jsonify(result), 400 if not result.get("success") else 200


def get_current_user():
    result = get_authenticated_user(request.headers.get("Authorization"))

    return jsonify(result), 200 if result.get("success") else 400


def get_authenticated_user(authorization: str | None):
    if not authorization:
        return {"success": False, "message": "Authorization header not found"}

    return user.get_current_user(authorization.split(" ")[1])
