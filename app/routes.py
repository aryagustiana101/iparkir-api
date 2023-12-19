from flask import Flask, jsonify, request

from app.auth import google_auth, google_auth_callback


def init(app: Flask):
    def index():
        return jsonify({"message": "Hello world!"})

    def unsupported(_):
        return jsonify({"message": "Unsupported request"}), 400

    def google_auth_handler():
        return jsonify(google_auth())

    def google_auth_callback_handler():
        code = f"{request.args.get('code')}"
        return jsonify(google_auth_callback(code))

    app.route("/")(index)
    app.errorhandler(404)(unsupported)
    app.errorhandler(405)(unsupported)

    app.route("/auth/google", methods=["POST"])(google_auth_handler)
    app.route("/auth/google/callback")(google_auth_callback_handler)
