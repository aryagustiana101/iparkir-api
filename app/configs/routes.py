from flask import Flask

import app.handlers as handlers
from app.libs.middleware import admin_user_route, protected_route


def init(app: Flask):
    app.before_request(protected_route)
    app.before_request(admin_user_route)

    app.route("/")(handlers.index)
    app.errorhandler(400)(handlers.unsupported)
    app.errorhandler(404)(handlers.unsupported)
    app.errorhandler(405)(handlers.unsupported)
    app.errorhandler(415)(handlers.unsupported)

    app.route("/auth/google", methods=["POST"])(handlers.auth.google_auth)
    app.route(
        rule="/auth/google/callback",
        methods=["POST", "GET"])(handlers.auth.google_auth_callback)

    app.route("/auth/logout", methods=["POST"])(handlers.auth.logout)

    app.route("/users/me", methods=["GET"])(handlers.users.get_current_user)

    app.route("/spots", methods=["GET"])(handlers.spots.get_spots)
    app.route("/spots/<id>", methods=["GET"])(handlers.spots.get_spot)
    app.route("/spots", methods=["POST"])(handlers.spots.create_spot)
    app.route(
        rule="/spots/<id>",
        methods=["PUT", "PATCH"])(handlers.spots.update_spot)
    app.route(
        rule="/spots/<id>",
        methods=["DELETE"])(handlers.spots.delete_spot)
    app.route(
        rule="/spots/<id>/reserve",
        methods=["POST"])(handlers.spots.reserve_spot)

    app.route(
        methods=["GET"],
        rule="/reservations")(handlers.reservations.get_reservations)

    app.route(
        methods=["GET"],
        rule="/reservations/<id>")(handlers.reservations.get_reservation)

    app.route(
        methods=["PUT", "PATCH"],
        rule="/reservations/<id>")(handlers.reservations.update_reservation)
