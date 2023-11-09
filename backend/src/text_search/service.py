import uuid
from datetime import datetime
from typing import Any

import httpx
from config import settings
from src.database import execute, search_history
from src.utils import LOGGER


async def text_search(user_id: int, query: str, size: int) -> dict[str, Any] | None:
    insert_query = search_history.insert().values(
        uuid=uuid.uuid4(),
        user_id=user_id,
        search_query=query,
        time=datetime.utcnow(),
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.TEXT_SEARCH_URL}/full-text-search?query={query}&size={size}"
            )

            if response.status_code == 200:
                search_results = response.json()

                # Save history
                await execute(insert_query)

                return search_results
            else:
                LOGGER.error(
                    f"Failed to call the API. Status code: {response.status_code} - {response.text}"
                )
        except Exception as e:
            LOGGER.error(f"An error occurred: {str(e)}")
