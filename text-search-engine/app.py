from config import settings
from elastic_search.searcher import ElasticSearcher
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from log_config import configure_logging
from schemas import Product

# Configure logging
logger = configure_logging(__name__)

# Create a FastAPI app instance with the specified title from settings
app = FastAPI(title=settings.APP_NAME)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ElasticSearcher
elastic_search = ElasticSearcher()


@app.get("/")
def healthcheck() -> bool:
    """Check the server's status."""
    return True


@app.get("/full-text-search", response_model=list[Product])
async def full_text_search(query: str, size: int):
    """
    Perform a full-text search based on the query.

    Args:
        query (str): The search query.
        size (int): The number of search results to retrieve.

    Returns:
        list: A list of search results as Product objects.
    """
    try:
        search_results = await elastic_search.text_search(query=query, top_k=size)

        result = [
            Product.from_point(suggestion["_source"]) for suggestion in search_results
        ]

        logger.info(f"Text search successful, query: {query}")

        return result

    except Exception as e:
        logger.error("Could not perform text search: %s", e)
        raise HTTPException(status_code=500, detail=e)


@app.get("/auto-complete-search", response_model=list[Product])
async def auto_complete_search(query: str, size: int):
    """
    Provide auto-complete suggestions based on the query.

    Args:
        query (str): The query for auto-complete suggestions.
        size (int): The number of auto-complete suggestions to retrieve.

    Returns:
        list: A list of auto-complete suggestions as Product objects.
    """
    try:
        search_results = await elastic_search.auto_complete(query=query, top_k=size)

        result = [
            Product.from_point(suggestion["_source"]) for suggestion in search_results
        ]

        logger.info(f"Auto-complete search successful, query: {query}")

        return result

    except Exception as e:
        logger.error("Could not perform auto-complete: %s", e)
        raise HTTPException(status_code=500, detail=e)
