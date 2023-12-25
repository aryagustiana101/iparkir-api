from flask import jsonify, request

from app.services import auth


def google_auth():
    return jsonify(auth.google_auth())


def google_auth_callback():
    result = auth.google_auth_callback(f"{request.args.get("code")}")

    return jsonify(result), 400 if not result.get("success") else 200
