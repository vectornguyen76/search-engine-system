from fastapi import APIRouter, Depends, File, UploadFile
from src.auth.jwt import parse_jwt_demo
from src.auth.schemas import JWTData
from src.image_search import service
from src.image_search.schemas import SearchResponse

router = APIRouter()


@router.post("/search", response_model=list[SearchResponse])
async def search(
    file: UploadFile = File(...), jwt_data: JWTData = Depends(parse_jwt_demo)
):
    result = await service.image_search(user_id=jwt_data.user_id, file=file)

    return result
