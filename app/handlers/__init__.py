from flask import jsonify

import app.handlers.auth as auth
import app.handlers.spots as spots
import app.handlers.users as users
import app.handlers.webhooks as webhooks
import app.handlers.reservations as reservations


def index():
    return jsonify({"success": True, "message": "Hello world!"})


def unsupported(_):
    return jsonify({"success": False, "message": "Unsupported request"}), 400
