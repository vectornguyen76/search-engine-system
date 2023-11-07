from config import settings
from fastapi import FastAPI
from src.auth import service
from src.auth.router import router as auth_router
from src.text_search.router import router as text_search_router

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
async def startup_event():
    await service.init_user(email=settings.ADMIN_EMAIL)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(text_search_router, prefix="/text_search", tags=["Text Search"])
