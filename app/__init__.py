from flask import Flask

from app.constants import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.json.sort_keys = False  # type: ignore
