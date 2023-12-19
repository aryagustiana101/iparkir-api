import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(f"{os.getenv("PORT")}")
SECRET_KEY = f"{os.getenv("SECRET_KEY")}"
PYTHON_ENV = f"{os.getenv("PYTHON_ENV")}"
GOOGLE_AUTH_URL = f"{os.getenv("GOOGLE_AUTH_URL")}"
GOOGLE_CLIENT_ID = f"{os.getenv("GOOGLE_CLIENT_ID")}"
GOOGLE_REDIRECT_URI = f"{os.getenv("GOOGLE_REDIRECT_URI")}"
GOOGLE_API_BASE_URL = f"{os.getenv("GOOGLE_API_BASE_URL")}"
GOOGLE_CLIENT_SECRET = f"{os.getenv("GOOGLE_CLIENT_SECRET")}"
