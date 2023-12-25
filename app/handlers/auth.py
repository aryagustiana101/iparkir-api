from flask import jsonify, request

from app.services import auth


def google_auth():
    return jsonify(auth.google_auth())


def google_auth_callback():
    result = auth.google_auth_callback(f"{request.args.get("code")}")

    return jsonify(result), 400 if not result.get("success") else 200


def logout():
    token = f"{request.headers.get("Authorization")}".split(" ")[1]

    result = auth.logout(token)

    return jsonify(result), 400 if not result.get("success") else 200
