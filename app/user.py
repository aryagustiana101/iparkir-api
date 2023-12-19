import jwt
from app.constants import SECRET_KEY


def get_current_user(token: str):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return {"success": True, "user": user}
    except:
        return {"success": False, "message": "Token invalid"}
