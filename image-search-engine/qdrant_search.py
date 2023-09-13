import numpy as np
from config import settings
from qdrant_client import QdrantClient, models

# Create a client to interact with Qdrant
client = QdrantClient(
    location= settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    prefer_grpc=True,
)
