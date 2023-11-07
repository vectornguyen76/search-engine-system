import uuid
from datetime import datetime
from typing import Any

import httpx
from config import settings
from src.database import execute, search_history
from src.text_search.schemas import SearchData


async def text_search(search_data: SearchData) -> dict[str, Any] | None:
    insert_query = search_history.insert().values(
        uuid=uuid.uuid4(),
        user_id=search_data.user_id,
        search_query=search_data.search_query,
        time=datetime.utcnow(),
    )

    async with httpx.AsyncClient() as client:
        query = search_data.search_query
        size = search_data.size

        response = await client.get(
            f"{settings.TEXT_SEARCH_URL}/full-text-search?query={query}&size={size}"
        )

        if response.status_code == 200:
            data = response.json()

            # Save history
            await execute(insert_query)

            return data
        else:
            print(f"Failed to call the API. Status code: {response.status_code}")
