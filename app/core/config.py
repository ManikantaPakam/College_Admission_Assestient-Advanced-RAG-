from pathlib import Path
from dotenv import load_dotenv
import os


# Project Base Directory
BASE_DIR = Path(__file__).resolve().parents[2]


# Load Environment Variables
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# Helper Function for Boolean Values
def get_bool_env(variable_name, default=False):

    value = os.getenv(variable_name)

    if value is None:
        return default

    return value.lower() in ("true", "1", "yes", "on")


# Application Environment
APP_ENV = os.getenv(
    "APP_ENV",
    "development"
).lower()


# Debug Configuration
DEBUG = get_bool_env(
    "DEBUG",
    APP_ENV == "development"
)


# Logging Configuration
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
).upper()


# API Documentation Configuration
API_DOCS_ENABLED = get_bool_env(
    "API_DOCS_ENABLED",
    APP_ENV != "production"
)


# Gemini API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Embedding Model Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


# ChromaDB Configuration
CHROMA_DB_DIR = BASE_DIR / os.getenv(
    "CHROMA_DB_DIR",
    "chroma_db"
)


COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "college_admission"
)

RATE_LIMIT = os.getenv(
    "RATE_LIMIT",
    "10/minute"
)

# JWT Authentication Configuration

JWT_ALGORITHM = "RS256"

JWT_ISSUER = os.getenv(
    "JWT_ISSUER",
    "college-admission-auth"
)

JWT_AUDIENCE = os.getenv(
    "JWT_AUDIENCE",
    "college-admission-rag"
)

JWT_PRIVATE_KEY_PATH = BASE_DIR / "private.pem"

JWT_PUBLIC_KEY_PATH = BASE_DIR / "app" / "core" / "public.pem"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7")
)

# DataBase URL
DATABASE_URL = os.getenv("DATABASE_URL")