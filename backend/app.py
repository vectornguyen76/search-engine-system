from config import settings
from fastapi import FastAPI
from src.auth.router import router as auth_router

app = FastAPI(title=settings.APP_NAME)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
