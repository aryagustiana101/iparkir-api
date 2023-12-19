from flask import Flask
import app.handler as handler


def init(app: Flask):
    app.route("/")(handler.index)
    app.errorhandler(404)(handler.unsupported)
    app.errorhandler(405)(handler.unsupported)

    app.route("/auth/google", methods=["POST"])(handler.google_auth)
    app.route("/auth/google/callback")(handler.google_auth_callback)

    app.route("/user/me", methods=["GET"])(handler.get_current_user)
