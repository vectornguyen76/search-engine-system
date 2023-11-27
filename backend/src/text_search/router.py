from fastapi import APIRouter, Depends
from src.auth.jwt import parse_jwt_demo
from src.auth.schemas import JWTData
from src.text_search import service
from src.text_search.schemas import SearchResponse

router = APIRouter()


@router.get("/search", response_model=list[SearchResponse])
async def search(query: str, size: int, jwt_data: JWTData = Depends(parse_jwt_demo)):
    result = await service.text_search(user_id=jwt_data.user_id, query=query, size=size)

    return result


@router.get("/auto-complete", response_model=list[SearchResponse])
async def auto_complete(
    query: str, size: int, jwt_data: JWTData = Depends(parse_jwt_demo)
):
    result = await service.auto_complete(
        user_id=jwt_data.user_id, query=query, size=size
    )

    return result
