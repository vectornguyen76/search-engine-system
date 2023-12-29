from typing import Any

import httpx
from config import settings
from fastapi import File, UploadFile
from src.utils import LOGGER


async def image_search(
    user_id: int, file: UploadFile = File(...)
) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            # Read the file content and prepare it for upload
            file_content = file.file.read()

            # Upload the image to the /search-image-qdrant endpoint
            files = {"file": ("image.jpg", file_content, "image/jpeg")}

            # Upload the image to the /search-image-qdrant endpoint
            response = await client.post(
                # f"{settings.IMAGE_SEARCH_URL}/search-image-qdrant", files=files
                f"{settings.IMAGE_SEARCH_URL}/search-image",
                files=files,
            )

            if response.status_code == 200:
                # Successful response, parse the results
                search_results = response.json()

                return search_results
            else:
                LOGGER.error(
                    f"Failed to call the API. Status code: {response.status_code} - {response.text}"
                )

        except Exception as e:
            LOGGER.error(f"An error occurred: {str(e)}")
