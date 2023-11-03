from config import settings
from fastapi import FastAPI
from src.db import Base, engine
from src.routers import user_router

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
