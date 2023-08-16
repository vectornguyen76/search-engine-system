# Image Search Engine on Shopee
This is a project about Image Retrieval. You can search Men Clothes on Shopee by image. It is the same as google image search

### Faiss 
To store a FAISS index and its associated data (vectors), you have a few options depending on your requirements:
- **In-Memory Storage**: You can keep the FAISS index and vectors in memory as long as your system has enough RAM to accommodate the data. This is the simplest and fastest option, but it might not be feasible for very large datasets.

- **Disk Storage**: If the entire dataset cannot fit into memory, you can save the FAISS index and vectors to disk using the serialization functionality provided by FAISS. This way, you can load the index back into memory when needed.

- **Database Storage**: For larger datasets that don't fit into memory, you can consider using databases to store the vectors and other metadata. Some popular databases for this purpose are SQLite, PostgreSQL, or MongoDB. In this approach, you would use the FAISS index to perform the search, but the actual vectors are stored and managed in the database.

### Problem
- Issue update faiss store with multiple workers or multiple pods.