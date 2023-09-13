import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))

# dotenv_path = os.path.join(basedir, ".env")

# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)

class Settings(BaseSettings):
    # App config
    APP_NAME: str = "API Image Search Engine"
    APP_ENV: str = "develop"
    
    # Logging setting
    DATE_FMT: str = '%Y-%m-%d %H:%M:%S'
    LOG_DIR: str = f'{basedir}/logs/api.log'
    
    IMAGEDIR:str = "assets/uploaded_images/"
    
    # Qdrant configuration
    QDRANT_URL:str = os.environ.get("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION:str = os.environ.get("QDRANT_COLLECTION", "image-search-engine")

    # Search configuration
    MAX_SEARCH_LIMIT:int = 100
    DEFAULT_LIMIT:int = 12
    GROUP_BY_FIELD:str = "cafe.slug"


settings = Settings()