import os
from dotenv import load_dotenv

load_dotenv()

AUTH_FILE_DATA = "./data/auth.json"
SPOTS_FILE_DATA = "./data/spots.json"
USERS_FILE_DATA = "./data/users.json"
ADMIN_USERS_FILE_DATA = "./data/admin-users.json"
RESERVATIONS_FILE_DATA = "./data/reservations.json"

CLI_PIN = f"{os.getenv("CLI_PIN")}"
APP_URL = f"{os.getenv("APP_URL")}"
SECRET_KEY = f"{os.getenv("SECRET_KEY")}"
PYTHON_ENV = f"{os.getenv("PYTHON_ENV")}"
PORT = int(f"{os.getenv("PORT") or 5000}")
GOOGLE_API_URL = f"{os.getenv("GOOGLE_API_URL")}"
GOOGLE_AUTH_URL = f"{os.getenv("GOOGLE_AUTH_URL")}"
GOOGLE_CLIENT_ID = f"{os.getenv("GOOGLE_CLIENT_ID")}"
STRIPE_SECRET_KEY = f"{os.getenv("STRIPE_SECRET_KEY")}"
GOOGLE_REDIRECT_URI = f"{os.getenv("GOOGLE_REDIRECT_URI")}"
GOOGLE_CLIENT_SECRET = f"{os.getenv("GOOGLE_CLIENT_SECRET")}"

CURRENCY = "IDR"
DEFAULT_FILE_DATA_FORMAT = {"increment": 0, "records": []}
