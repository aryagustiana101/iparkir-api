from flask import jsonify, request

from app.services.auth import check_admin_user, get_authenticated_user


def protected_route():
    view_args = request.view_args or {}

    protected_routes = {
        "/users/me": ["GET"],
        "/auth/logout": ["POST"],
        "/spots": ["GET", "POST"],
        f"/spots/{view_args.get("id") or "<id>"}/reserve": ["POST"],
        f"/spots/{view_args.get("id") or "<id>"}": ["GET", "PUT", "PATCH", "DELETE"],
    }

    if \
            request.path in protected_routes.keys() and \
            request.method in protected_routes[request.path]:

        result = get_authenticated_user(request.headers.get("Authorization"))

        if not result.get("success"):
            return jsonify(result), 401


def admin_user_route():
    view_args = request.view_args or {}

    protected_routes = {
        "/spots": ["POST"],
        f"/spots/{view_args.get("id") or "<id>"}": ["PUT", "PATCH", "DELETE"],
    }

    if \
            request.path in protected_routes.keys() and \
            request.method in protected_routes[request.path]:

        user = get_authenticated_user(
            request.headers.get("Authorization")
        ).get("data")

        if user is None or (not check_admin_user(user.get("user_id"))):
            return jsonify({
                "success": False,
                "message": "You are not authorized to perform this action",
            }), 401
