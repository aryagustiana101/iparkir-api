from flask import Flask, jsonify


def init(app: Flask):
    def index():
        return jsonify({"message": "Hello world!"})

    def not_found(_):
        return jsonify({"message": "Unsupported request"})

    app.route("/")(index)
    app.errorhandler(404)(not_found)
