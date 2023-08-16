import os
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))

class Settings(BaseSettings):
    # App config
    APP_NAME: str = "FastAPI Rest API Template"
    APP_ENV: str = "develop"
    
    # Logging setting
    DATE_FMT: str = '%Y-%m-%d %H:%M:%S'
    LOG_DIR: str = f'{basedir}/logs/api.log'
    
    # Database config
    SQLALCHEMY_DATABASE_URL:str = "postgresql+psycopg2://postgres:070600@localhost/db_shopee"
    # SQLALCHEMY_DATABASE_URL:str = "postgresql+psycopg2://db_user:db_password@localhost/db_shopee"

settings = Settings()