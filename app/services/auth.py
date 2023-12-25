import jwt
import requests
import urllib.parse
from datetime import datetime

from app import constants
from app.services import users
from app.utils import binary_search, read_file_data, rewrite_file_data


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

    file_data = read_file_data(constants.AUTH_FILE_DATA)

    increment = (file_data.get("increment") or 0) + 1

    rewrite_file_data(constants.AUTH_FILE_DATA, {
        **file_data,
        "increment": increment,
        "records": [
            *(file_data.get("records") or []),
            {
                "id": increment,
                "token": token,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        ],
    })

    return {"success": True, "token": token}


def logout(token: str):
    file_data = read_file_data(constants.AUTH_FILE_DATA)

    rewrite_file_data(constants.AUTH_FILE_DATA, {
        **file_data,
        "records": [
            record for record in (file_data.get("records") or [])
            if record["token"] != token
        ],
    })

    return {"success": True, "message": "Logged out"}


def get_authenticated_user(authorization: str | None):
    if not authorization:
        return {"success": False, "message": "Authorization header not found"}

    token = authorization.split(" ")[1]

    file_data = read_file_data(constants.AUTH_FILE_DATA)

    result = binary_search(
        search=token,
        key_function=lambda x: x["token"],
        data=(file_data.get("records") or []),
    )

    if not result:
        return {"success": False, "message": "Token not found"}

    return users.get_current_user(token=token)


def check_admin_user(id: str):
    file_data = read_file_data(constants.ADMIN_USERS_FILE_DATA)

    admin = binary_search(
        search=id,
        key_function=lambda x: x["user_id"],
        data=file_data.get("records") or [],
    )

    return admin is not None
