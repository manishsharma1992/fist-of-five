import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

load_dotenv()

def get_encryption_key() -> str:
    """
    Retrieves the encryption key from the environment variables.
    If not set, generates a new Fernet Key and sets it in the environment variables
    :return: Fernet Key
    """
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        key = Fernet.generate_key()
        key = key.decode("utf-8")
        os.environ['ENCRYPTION_KEY'] = key
    return key


def get_decrypted_password(encrypted_password: str) -> str:
    """
    Decrypts the password using the encryption key
    :param encrypted_password: Encrypted Password
    :return: Decrypted Password
    """
    key = get_encryption_key().encode("utf-8")
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")


# Read credentials from environment variables
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_NAME = os.environ.get('DATABASE')
encrypted_password = os.environ.get('DATABASE_PASSWORD')

if not all([DATABASE_HOST, DATABASE_USERNAME, DATABASE_NAME, encrypted_password]):
    raise ValueError("Database credentials not set in the environment variables")

# Decrypt the password
DATABASE_PASSWORD = get_decrypted_password(encrypted_password)

# Use PyMySQL driver with SSL certificate passed via the query parameter.
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Additional engine options (here, only autocommit is passed)
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "max_overflow": 20,
}

# Instantiate the SQLAlchemy Engine
db = SQLAlchemy()
