from flask import jsonify, request

from app.services.auth import get_authenticated_user


def protected_route():
    view_args = request.view_args or {}

    protected_routes = {
        "/users/me": ["GET"],
        "/spots": ["GET", "POST"],
        f"/spots/{view_args.get("id") or "<id>"}": ["GET", "PUT", "PATCH", "DELETE"],
    }

    if \
            request.path in protected_routes.keys() and \
            request.method in protected_routes[request.path]:

        result = get_authenticated_user(request.headers.get("Authorization"))

        if not result.get("success"):
            return jsonify(result), 401
