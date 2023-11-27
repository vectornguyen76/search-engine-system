import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))

ENVIRONMENT = os.getenv(key="ENVIRONMENT", default="DEVELOP")

if ENVIRONMENT == "DEVELOP":
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

    SITE_DOMAIN: str = "vectornguyen.com"

    ADMIN_EMAIL: str = "vectornguyen76@gmail.com"

    TEXT_SEARCH_URL: str = os.getenv(
        key="TEXT_SEARCH_URL", default="http://localhost:8000"
    )
    IMAGE_SEARCH_URL: str = os.getenv(
        key="IMAGE_SEARCH_URL", default="http://localhost:7000"
    )


settings = Settings()
