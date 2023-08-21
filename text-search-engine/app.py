from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from config import settings

# Create a FastAPI app instance with the specified title from settings
app = FastAPI(title=settings.APP_NAME)

# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Elasticsearch
elastic_search = Elasticsearch(settings.ELASTICSEARCH_HOST)

@app.get("/full-text-search")
async def full_text_search(query: str, size: int):
    """
    Endpoint to perform a full-text search based on the query.

    Args:
        query (str): The search query.
        size (int): The number of search results to retrieve.

    Returns:
        dict: A dictionary containing the search results.
    """
    index_name = 'text_search_index'
    
    # Define a search query
    search_query = {
        'size': size,
        'query': {
            'match': {
                'item_name': query 
            }
        }
    }

    # Perform the search
    search_results = elastic_search.search(index=index_name, body=search_query)

    results = []
    for suggestion in search_results['hits']['hits']:
        results.append(suggestion["_source"])

    return {"results": results}

@app.get("/auto-complete-search")
async def auto_complete_search(query: str, size: int):
    """
    Endpoint to provide auto-complete suggestions based on the query.

    Args:
        query (str): The query for which auto-complete suggestions are requested.
        size (int): The number of auto-complete suggestions to retrieve.

    Returns:
        dict: A dictionary containing the auto-complete suggestions.
    """
    index_name = 'text_search_index'
    
    # Build the search request
    search_request = {
        "suggest": {
            "item-suggest": {
                "prefix": query,
                "completion": {
                    "field": "item_name.suggest",
                    "size": size
                }
            }
        }
    }

    # Perform the search
    results = elastic_search.search(index=index_name, body=search_request)

    # Extract and format the suggestions
    suggestions = results["suggest"]["item-suggest"][0]["options"]
    
    formatted_results = []
    for suggestion in suggestions:
        formatted_results.append(suggestion["_source"])
        
    return {"results": formatted_results}
