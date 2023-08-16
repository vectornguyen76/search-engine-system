import faiss
import faiss_config
import numpy as np
import pandas as pd

class FaissSearch():
    def __init__(self):
        """
        Initializes the FaissSearch class.

        This class provides functionality to perform similarity search using the Faiss library.

        Attributes:
        - index (faiss.Index): The Faiss index used for search.
        - data (pd.DataFrame): The dataset used for indexing and searching.
        """
        self.index = faiss.read_index(faiss_config.INDEX_PATH)
        self.data = pd.read_csv(faiss_config.DATA_PATH, header=None)
    
    def search(self, query_vector, top_k=faiss_config.TOP_K):
        """
        Performs a similarity search using the provided query vector.

        Args:
        - query_vector (np.ndarray): The query vector for similarity search.
        - top_k (int, optional): The number of nearest neighbors to retrieve. Default is specified in faiss_config.

        Returns:
        - np.ndarray: An array of distances from the query vector to the nearest neighbors.
        - np.ndarray: An array of indices representing the positions of the nearest neighbors in the dataset.
        """
        distances, indices = self.index.search(query_vector, top_k)
        return distances, indices
    

if __name__ == "__main__":
    # Instantiate the FaissSearch class
    faiss_search = FaissSearch()
    
    # Create a random query vector
    num_vectors = 1
    dimension = 1000
    vector = np.random.rand(num_vectors, dimension).astype('float32')
    
    print("shape vector", vector.shape)
    
    # Perform a similarity search using the query vector
    distances, indices = faiss_search.search(query_vector=vector, top_k=3)
    
    print("distance", distances)
    print("indices", indices)
