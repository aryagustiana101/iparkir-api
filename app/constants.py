import os
from dotenv import load_dotenv

load_dotenv()

CLI_PIN = f"{os.getenv("CLI_PIN")}"
AUTH_FILE_DATA = "./data/auth.json"
SPOTS_FILE_DATA = "./data/spots.json"
SECRET_KEY = f"{os.getenv("SECRET_KEY")}"
PYTHON_ENV = f"{os.getenv("PYTHON_ENV")}"
PORT = int(f"{os.getenv("PORT") or 5000}")
ADMIN_USERS_FILE_DATA = "./data/admin-users.json"
GOOGLE_API_URL = f"{os.getenv("GOOGLE_API_URL")}"
GOOGLE_AUTH_URL = f"{os.getenv("GOOGLE_AUTH_URL")}"
GOOGLE_CLIENT_ID = f"{os.getenv("GOOGLE_CLIENT_ID")}"
GOOGLE_REDIRECT_URI = f"{os.getenv("GOOGLE_REDIRECT_URI")}"
GOOGLE_CLIENT_SECRET = f"{os.getenv("GOOGLE_CLIENT_SECRET")}"
