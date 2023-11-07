from fastapi import APIRouter
from src.text_search import service
from src.text_search.schemas import SearchData, SearchResponse

router = APIRouter()


@router.get("/search", response_model=list[SearchResponse])
async def search(search_data: SearchData):
    result = await service.text_search(search_data=search_data)

    return result
