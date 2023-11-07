import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    # App config
    APP_NAME: str = "FastAPI Rest API Template"
    APP_ENV: str = "develop"
    APP_VERSION: str = "1"

    # Logging setting
    DATE_FMT: str = "%Y-%m-%d %H:%M:%S"
    LOG_DIR: str = f"{basedir}/logs/api.log"

    # Database config
    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = "myapp.com"

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    ADMIN_EMAIL: str = "vectornguyen76@gmail.com"


settings = Settings()
