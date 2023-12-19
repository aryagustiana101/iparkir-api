import requests
import urllib.parse
from app.constants import GOOGLE_API_URL, GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI


def google_auth():
    search_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "email profile openid",
        "response_type": "code",
    }

    return {"redirect_url": f"{GOOGLE_AUTH_URL}/auth?{urllib.parse.urlencode(search_params)}"}


def google_auth_callback(code: str):
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response_token = requests.post(f"{GOOGLE_AUTH_URL}/token", data=token_data)

    if response_token.status_code != 200:
        print(response_token.json())
        return {"success": False, "message": "Failed to retrieve access token"}

    access_token = response_token.json().get("access_token")

    if not access_token:
        return {"success": False, "message": "Access token not found in response"}

    user_info_response = requests.get(
        f"{GOOGLE_API_URL}/userinfo?access_token={access_token}")

    if user_info_response.status_code != 200:
        print(user_info_response.json())
        return {"success": False, "message": "Failed to fetch user information"}

    user_info = user_info_response.json()

    return {"success": True, "user_info": user_info}
