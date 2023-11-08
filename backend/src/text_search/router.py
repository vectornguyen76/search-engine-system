from fastapi import APIRouter, Depends
from src.auth.jwt import parse_jwt_demo
from src.auth.schemas import JWTData
from src.text_search import service
from src.text_search.schemas import SearchData, SearchResponse

router = APIRouter()


@router.get("/search", response_model=list[SearchResponse])
async def search(search_data: SearchData, jwt_data: JWTData = Depends(parse_jwt_demo)):
    result = await service.text_search(
        user_id=jwt_data.user_id, search_data=search_data
    )

    return result