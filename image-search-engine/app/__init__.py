from fastapi import FastAPI
from app.db import Base, engine
from app.routers import user_router
from config import settings
from app.logging import configure_logging
import logging

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

configure_logging(name=__name__)