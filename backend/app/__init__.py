import logging

from app.db import Base, engine
from app.logging import configure_logging
from app.routers import user_router
from config import settings
from fastapi import FastAPI

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

configure_logging(name=__name__)
