from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")