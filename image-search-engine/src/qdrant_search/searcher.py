import asyncio

import numpy as np
from config import settings
from qdrant_client import QdrantClient, grpc
from src.decorators import async_time_profiling, time_profiling


class QdrantSearch:
    """
    A class for performing similarity search in Qdrant.

    Attributes:
        client_grpc (QdrantClient): A client for interacting with Qdrant.
    """

    # @time_profiling
    def __init__(self):
        """
        Initializes a QdrantSearch instance and creates a Qdrant client.
        """
        # Create a client to interact with Qdrant
        self.client_grpc = QdrantClient(url=settings.QDRANT_URL, prefer_grpc=True)

    @async_time_profiling
    async def search(self, query_vector, top_k=settings.TOP_K):
        """
        Performs a similarity search in Qdrant using a query vector.

        Args:
            query_vector (numpy.ndarray): The query vector for similarity search.
            top_k (int): The number of top results to retrieve (default is settings.TOP_K).

        Returns:
            grpc.SearchPointsResponse: The response from Qdrant containing search results.
        """
        response = await self.client_grpc.async_grpc_points.Search(
            grpc.SearchPoints(
                collection_name=settings.QDRANT_COLLECTION,
                vector=query_vector[0],
                limit=top_k,
                with_payload=grpc.WithPayloadSelector(enable=True),
            )
        )

        return response


if __name__ == "__main__":
    # Instantiate the QdrantSearch class
    qdrant_search = QdrantSearch()

    # Create a random query vector
    dimension = 1000
    vector = np.random.rand(dimension).astype("float32")

    print("Query vector shape:", vector.shape)

    # Perform a similarity search using the query vector
    asyncio.run(qdrant_search.search(query_vector=vector, top_k=3))
