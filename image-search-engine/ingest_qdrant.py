from qdrant_client import grpc
from config import settings
from qdrant_client import QdrantClient, models
import numpy as np
import pandas as pd
import asyncio
import time

# Load array features
array_features = np.load("./data/array_features.npz", allow_pickle=True)

# Extract attributes from the dataset
df = pd.read_csv("./data/data.csv", header=None)
item_url = df.values[:, 0]
item_image = df.values[:, 1]
item_name = df.values[:, 2]
item_price = df.values[:, 3]


async def main():
    # Create a client to interact with Qdrant
    client = QdrantClient("localhost")

    # Create collection
    response = await client.async_grpc_collections.Create(
        grpc.CreateCollection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=grpc.VectorsConfig(
                params=grpc.VectorParams(
                    size=1000,
                    distance=grpc.Distance.Cosine,
                )
            ),
            quantization_config=grpc.QuantizationConfig(
                scalar=grpc.ScalarQuantization(
                    type=grpc.QuantizationType.Int8,
                    always_ram=False,
                )
            ),
            timeout=10,
            # shard_number=2,
        )
    )
    
    print("Done create collection!")
    print(response)
    
    
    start_time = time.time()
    list_point = []
    for index in range(10):
        list_point.append(grpc.PointStruct(
            id=index,
            payload={
                "item_url": item_url[index],
                "item_image": item_image[index],
                "item_name": item_name[index],
                "item_price": item_price[index],
            },
            vectors=grpc.Vectors(
                vector=grpc.Vector(data=array_features['array_features'][index].tolist()),
            )
        ))
        
        # list_point.append(grpc.PointStruct(
        #     id=grpc.PointId(num=index),
        #     payload={
        #         "item_url": grpc.Value(string_value=item_url[index]),
        #         "item_image": grpc.Value(string_value=item_image[index]),
        #         "item_name": grpc.Value(string_value=item_name[index]),
        #         "item_price": grpc.Value(string_value=item_price[index]),
        #     },
        #     vectors=grpc.Vectors(
        #         vector=grpc.Vector(data=array_features['array_features'][index].tolist()),
        #     ),
        # ))
        # list_point.append(grpc.PointVectors(
        #     id=grpc.PointId(num=index),
        #     vectors=grpc.Vectors(
        #         vector=grpc.Vector(data=array_features['array_features'][index].tolist()),
        #     ),
        # ))
    total_time = time.time() - start_time
    print(f"Done create list point!")
    print(f"time: {total_time:.2f}\n")
    
    # Add to qdrant
    response = await client.async_grpc_points.Upsert(
        grpc.UpsertPoints(
            collection_name=settings.QDRANT_COLLECTION,
            points=list_point,
        )
    )

    print("Add to qdrant successfully!")
    print(response)
    
asyncio.run(main())
