from flask import jsonify
from app.services import analytics


def get_analytics():
    return jsonify(analytics.get_analytics()), 200
