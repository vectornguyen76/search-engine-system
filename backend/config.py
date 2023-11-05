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

    # Logging setting
    DATE_FMT: str = "%Y-%m-%d %H:%M:%S"
    LOG_DIR: str = f"{basedir}/logs/api.log"

    # Database config
    DATABASE_URL: PostgresDsn


settings = Settings()
