from fastapi import FastAPI
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
# Connect to Elasticsearch
es = Elasticsearch()

app = FastAPI()

@app.post("/search")
async def search(query: str):
    index_name = 'text_search_index'
    
    # Define a search query
    search_query = {
        'query': {
            'match': {
                'item_name': query  # Search for documents with this value in the 'field_name' field
            }
        }
    }

    # Perform the search
    search_results = es.search(index=index_name, body=search_query)

    # Print the search results
    for hit in search_results['hits']['hits']:
        print(hit['_source'])

    return {"results": search_results['hits']['hits']}

@app.post("/auto-complete")
async def search_auto_complete(query: str):
    index_name = 'text_search_index'
    
    # Build the search request
    search_request = {
        "suggest": {
            "item-suggest": {
                "prefix": query,
                "completion": {
                    "field": "item_name.suggest",
                    "size": 5
                }
            }
        }
    }

    # Perform the search
    results = es.search(index=index_name, body=search_request)

    # Extract and print the suggestions
    suggestions = results["suggest"]["item-suggest"][0]["options"]
    
    results = []
    for suggestion in suggestions:
        print(suggestion["_source"]["item_name"])
        results.append(suggestion["_source"])
        
    return {"results": results}