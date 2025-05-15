from datetime import timedelta
from os import getenv
from dotenv import load_dotenv
import pathlib

load_dotenv()

DEBUG = False

DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")
COOKIE_LIFETIME = timedelta(seconds=5).total_seconds()

# Compose

APP_STORAGE = "storage/"
