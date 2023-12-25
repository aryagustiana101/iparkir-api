import jwt
import requests
import urllib.parse

from app import constants
from app.services import users


def google_auth():
    search_params = {
        "client_id": constants.GOOGLE_CLIENT_ID,
        "redirect_uri": constants.GOOGLE_REDIRECT_URI,
        "scope": "email profile openid",
        "response_type": "code",
    }

    return {
        "success": True,
        "redirect_url": f"{constants.GOOGLE_AUTH_URL}/auth?{urllib.parse.urlencode(search_params)}"
    }


def google_auth_callback(code: str):
    access_token_response = requests.post(
        url=f"{constants.GOOGLE_AUTH_URL}/token",
        data={
            "code": code,
            "client_id": constants.GOOGLE_CLIENT_ID,
            "client_secret": constants.GOOGLE_CLIENT_SECRET,
            "redirect_uri": constants.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
    )

    if access_token_response.status_code != 200:
        print(access_token_response.json())
        return {"success": False, "message": "Failed to retrieve access token"}

    access_token = access_token_response.json().get("access_token")

    if not access_token:
        return {"success": False, "message": "Access token not found in response"}

    user_info_response = requests.get(
        url=f"{constants.GOOGLE_API_URL}/userinfo?access_token={access_token}"
    )

    if user_info_response.status_code != 200:
        print(user_info_response.json())
        return {"success": False, "message": "Failed to fetch user information"}

    token = jwt.encode(
        algorithm="HS256",
        key=constants.SECRET_KEY,
        payload=user_info_response.json(),
    )

    return {"success": True, "token": token}


def get_authenticated_user(authorization: str | None):
    if not authorization:
        return {"success": False, "message": "Authorization header not found"}

    return users.get_current_user(token=authorization.split(" ")[1])
