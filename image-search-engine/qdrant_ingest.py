from qdrant_client import grpc
from config import settings
from qdrant_client import QdrantClient
import numpy as np
import pandas as pd
import time
from tqdm import tqdm

class QdrantIngest:
    """
    A class for ingesting data into Qdrant.

    Attributes:
        client_grpc (QdrantClient): A client for interacting with Qdrant.
        item_url (numpy.ndarray): Array of item URLs.
        item_image (numpy.ndarray): Array of item images.
        item_name (numpy.ndarray): Array of item names.
        item_price (numpy.ndarray): Array of item prices.
        array_features (numpy.ndarray): Array of features to be ingested.
    """
    def __init__(self):
        """
        Initializes a QdrantIngest instance, creates a Qdrant client, and loads data.
        """
        # Create a client to interact with Qdrant
        self.client_grpc = QdrantClient(url=settings.QDRANT_GRPC_URL, prefer_grpc=True)
        
        # Load the dataset
        data = pd.read_csv(settings.DATA_PATH, header=None)
        
        # Extract attributes from the dataset
        self.item_url = data.values[:, 0]
        self.item_image = data.values[:, 1]
        self.item_name = data.values[:, 2]
        self.item_price = data.values[:, 3]

        # Load array features
        self.array_features = np.load(settings.FEATURES_PATH, allow_pickle=True)

    def create_collection(self):
        """
        Creates a collection in Qdrant.

        Returns:
            grpc.CreateCollectionResponse: The response from Qdrant after creating the collection.
        """
        # Create collection
        response = self.client_grpc.grpc_collections.Create(
            grpc.CreateCollection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=grpc.VectorsConfig(
                    params=grpc.VectorParams(
                        size=settings.DIMENSIONS,
                        distance=grpc.Distance.Cosine,
                    )
                ),
                timeout=10
            )
        )
        
        return response

    def check_collection(self):
        """
        Checks if the collection already exists in Qdrant.

        Returns:
            grpc.GetCollectionInfoResponse: The response from Qdrant containing collection information.
        """
        response = self.client_grpc.grpc_collections.Get(
            grpc.GetCollectionInfoRequest(
                collection_name=settings.QDRANT_COLLECTION
            )
        )
        return response

    def add_points(self, batch_size=1000):
        """
        Adds data points to the Qdrant collection.

        Args:
            batch_size (int): Batch size for uploading data points.

        Returns:
            None
        """
        start_time = time.time()
        
        num_features = self.array_features['array_features'].shape[0]
        num_batches = (num_features + batch_size - 1) // batch_size
        
        for i in tqdm(range(num_batches)):
            # Split into batches
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, num_features)
            
            ids = list(range(start_idx, end_idx))
            payloads = [{"item_url": self.item_url[idx],
                        "item_image": self.item_image[idx],
                        "item_name": self.item_name[idx],
                        "item_price": self.item_price[idx]} 
                        for idx in range(start_idx, end_idx)]
            
            vectors = self.array_features['array_features'][start_idx: end_idx]
            
            self.client_grpc.upload_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors=vectors,
                payload=payloads,
                ids=ids
            )
            
        print("Done adding points to the collection!")
        print(f"Time: {time.time() - start_time}")

if __name__ == "__main__":
    # Instantiate the QdrantIngest class
    qdrant_ingest = QdrantIngest()
    
    try: 
        response = qdrant_ingest.check_collection()
        if response.result.status == 1:
            print(f"Collection {settings.QDRANT_COLLECTION} already exists!")
    except Exception as e:
        print(f"Error checking collection: {e}")
        
        response = qdrant_ingest.create_collection()
        print(response)
        
        qdrant_ingest.add_points()
