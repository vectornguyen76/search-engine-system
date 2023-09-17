# Image Search Engine on Shopee
### About solution
- Use qdrant instead of faiss because I want to start with small server. It run on CPU and scale when has a lot traffic

## Vector Database - Vector Search
### Faiss
1. **Overview**
    - Faiss is a library for efficient similarity search and clustering of dense vectors. It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM. Faiss is written in C++ with complete wrappers for Python/numpy. 
    - Faiss is particularly useful, such as recommendation systems, image retrieval, and more.

2. **Key Features**
    - **Distance Metrics**: Faiss supports L2 (Euclidean) distances, dot products, and cosine similarity for comparing vectors.
    - **GPU Support**:
        + *GPU Implementation*: Faiss provides GPU support for efficient vector search.
        + *Compatibility*: Faiss seamlessly handles input from both CPU and GPU memory.
        + *Performance*: Faiss can significantly boost performance when both input and output remain resident on the GPU.
        + *Multi-GPU Usage*: Faiss supports both single and multi-GPU usage

3. **Disadvantage**
    - Not support update it in real-time. You have to create your custom wrapper around it or use framework to support CRUD, high availability, horizontal scalability, concurrent access, and so on.

4. **Refrence**
    - https://github.com/facebookresearch/faiss

### Vector Search in ElasticSearch
1. **Overview**
    ElasticSearch is a popular search engine used by developers to implement search functionality in their applications. With each new release, Vector Search allows developers to search for documents based on their semantic similarity instead of just their textual relevance. This feature has many use cases, including semantic search, recommendation systems, image search and question answering.

2. **Disadvantage**
    - Not support GPU but can use plugin of third party.
    - Elasticsearch is typically way slower than all the competitors, no matter the dataset and metric.
    - Not support to batch vector search

3. **Pricing** 
    - Store embeddings and Search embeddings are free
    - Embedding models or Built-in semantic search model is paid
    - Price 125$/month for Machine learning

4. **Example**
    - **Create the index**
        ```shell
        PUT my-index
        {
            "mappings": {
                "properties": {
                    "my_vector": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": true,
                        "similarity": "cosine"

                    },
                    "my_text" : {
                        "type" : "text"
                    }
                }
            }
        }
        ```
    - **Index a document**
        ```shell
        PUT my-index/_doc/1
        {
            "my_vector" : [0.5, 10, 6, ….],
            "my_text" :"Jamaica's tropical climate brings warmth all year round"
        }
        ```
    - **Run vector search with deployed text embedding model**
        ```shell
        POST my-index/_search
        {
            "knn": {
                "field": "my_vector",
                "query_vector_builder": {
                    "text_embedding": {
                        "model_id": "sentence-transformers__all-minilm-l6-v2",
                        "model_text": "How is the weather in Jamaica?"
                    }
                },
                "k": 10,
                "num_candidates": 100
            }
        }
        ```
    - **Run vector search directly**
        ```shell
        POST my-index/_search
        {
            "knn": {
                "field": "my_vector",
                "query_vector": [0.3, 0.1, 1.2, ...],
                "k": 10,
                "num_candidates": 100
            },
        }
        ```

5. **Refrence**
    - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html#knn-semantic-search
    - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search-api.html

### Qdrant
1. **Overview**
    - Qdrant is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search, and manage points—vectors with an additional payload Qdrant is tailored to extended filtering support. It makes it useful for all sorts of neural-network or semantic-based matching, faceted search, and other applications.

    - Qdrant is written in Rust 🦀, which makes it fast and reliable even under high load.

2. **Advance**
    - Implement a unique custom modification of the HNSW algorithm for Approximate Nearest Neighbor Search. Search with a State-of-the-Art speed and apply search filters without compromising on results.
    - QDrant supports both CPU and GPU-based computing, making it highly flexible and adaptable to different hardware configurations.
    - It is highly scalable, is able to handle large-scale data and high user concurrency.
    - Support to batch vector search

3. **Disadvance**

4. **Beachmarks**
    <p align="center">
    <img src="./assets/benchmarks.jpg" alt="animated" />
    <br>
    <em>Batching Architecture</em>
    </p>

5. **Refrence**
    - https://qdrant.tech/benchmarks/
    - https://blog.qdrant.tech/batch-vector-search-with-qdrant-8c4d598179d5
    - https://github.com/qdrant/qdrant/issues/1656

## Environments
### Develop
1. **Create environment and install packages**
    ```shell
    conda create -n image-search python=3.9
    ```
    ```shell
    conda activate image-search
    ```
    ```shell
    pip install -r requirements.txt
    ```

2. **Run app**
    ```
    uvicorn app:app
    ```

### Result 
- Create and add 100.000 points in 6 minutes in qdrant
- p95: 


### Future
    - Inference batching (GPU)
    - Search batching
    - Improve model (Focus product)

<p align="center">
<img src="./assets/batching-architecture.png" alt="animated" />
<em>Batching Architecture</em>
</p>
<br>

- [BentoML](https://docs.bentoml.org/en/latest/guides/batching.html)
- https://www.bentoml.com/blog/bentoml-or-triton-inference-server-choose-both