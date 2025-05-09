from datetime import timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEBUG = False
DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")
COOKIE_LIFETIME = timedelta(hours=24).total_seconds()