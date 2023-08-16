import numpy as np
import faiss

# Generate random vectors for demonstration purposes
num_vectors = 1000
dimension = 128
vectors = np.random.rand(num_vectors, dimension).astype('float32')

# Create an index with FAISS
index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean distance) as similarity metric
index.add(vectors)

# Save the index to disk
index_filename = "index.faiss"
faiss.write_index(index, index_filename)

# Load the index from disk
loaded_index = faiss.read_index(index_filename)

# Define a query vector for similarity search
query_vector = np.random.rand(1, dimension).astype('float32')

# Perform the search with the loaded index
k = 5
distances, indices = loaded_index.search(query_vector, k)

# Results
print("Query vector:")
print(query_vector)
print("\nNearest neighbors:")
print(vectors[indices[0]])  # Printing the vectors of the nearest neighbors
print("\nDistances to nearest neighbors:")
print(distances[0])
