from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
SECRET = os.environ.get("SECRET")
SECRET_AUTH = os.environ.get("SECRET_AUTH")
RESET_PASSWORD_TOKEN_SERVER = os.environ.get("RESET_PASSWORD_TOKEN_SERVER")
VERIFICATION_TOKEN_SERVER = os.environ.get("VERIFICATION_TOKEN_SERVER")
