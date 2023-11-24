from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import service
from src.auth.router import router as auth_router
from src.image_search.router import router as image_search_router
from src.text_search.router import router as text_search_router

app = FastAPI(title=settings.APP_NAME)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await service.init_user(email=settings.ADMIN_EMAIL)


@app.get("/healthz")
async def healthcheck() -> bool:
    return True


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(text_search_router, prefix="/text_search", tags=["Text Search"])
app.include_router(image_search_router, prefix="/image_search", tags=["Image Search"])
