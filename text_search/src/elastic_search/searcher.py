import asyncio

from config import settings
from elasticsearch import AsyncElasticsearch


class ElasticSearcher:
    """Interacts with Elasticsearch for text search and auto-complete queries."""

    def __init__(self):
        """Initialize and connect to Elasticsearch."""
        self.elasticsearch = AsyncElasticsearch(settings.ELASTICSEARCH_HOST)

    async def text_search(self, query, top_k=settings.TOP_K):
        """
        Perform a text search in Elasticsearch.

        Args:
            query (str): The search query.
            top_k (int): Maximum number of results to retrieve.

        Returns:
            list: List of search results.
        """
        search_query = {
            "id": "fuzzy-search",
            "params": {"query_size": top_k, "query_string": query},
        }

        results = await self.elasticsearch.search_template(
            index=settings.INDEX_NAME, body=search_query
        )
        return results["hits"]["hits"]

    async def auto_complete(self, query, top_k=settings.TOP_K):
        """
        Perform an auto-complete search in Elasticsearch.

        Args:
            query (str): The auto-complete query.
            top_k (int): Maximum number of suggestions to retrieve.

        Returns:
            list: List of auto-complete suggestions.
        """
        search_query = {
            "suggest": {
                "item-suggest": {
                    "prefix": query,
                    "completion": {"field": "item_name.completion", "size": top_k},
                }
            }
        }
        results = await self.elasticsearch.search(
            index=settings.INDEX_NAME, body=search_query
        )
        return results["suggest"]["item-suggest"][0]["options"]


if __name__ == "__main__":
    elastic_search = ElasticSearcher()
    query = "Áo sơ mi"
    asyncio.run(elastic_search.text_search(query, top_k=3))
