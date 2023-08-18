import faiss
import faiss_config
import numpy as np
import pandas as pd

class FaissSearch:
    def __init__(self):
        """
        Initializes the FaissSearch class.

        This class provides functionality to perform similarity search using the Faiss library.

        Attributes:
        - index (faiss.Index): The Faiss index used for search.
        - item_url (np.ndarray): URLs of items in the dataset.
        - item_image (np.ndarray): Image paths of items in the dataset.
        - item_name (np.ndarray): Names of items in the dataset.
        - item_price (np.ndarray): Prices of items in the dataset.
        """
        # Load the dataset
        data = pd.read_csv(faiss_config.DATA_PATH, header=None)
        
        # Read the Faiss index
        self.index = faiss.read_index(faiss_config.INDEX_PATH)
        
        # Extract attributes from the dataset
        self.item_url = data.values[:, 0]
        self.item_image = data.values[:, 1]
        self.item_name = data.values[:, 2]
        self.item_price = data.values[:, 3]
           
    def search(self, query_vector, top_k=faiss_config.TOP_K):
        """
        Performs a similarity search using the provided query vector.

        Args:
        - query_vector (np.ndarray): The query vector for similarity search.
        - top_k (int, optional): The number of nearest neighbors to retrieve. Default is specified in faiss_config.

        Returns:
        - dict: A dictionary containing search results, including item information.
        """
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        
        for idx in indices[0]:
            results.append({
                "item_url": self.item_url[idx],
                "item_image": self.item_image[idx],
                "item_name": self.item_name[idx],
                "item_price": self.item_price[idx],
            })
        
        return {"results": results}
    

if __name__ == "__main__":
    # Instantiate the FaissSearch class
    faiss_search = FaissSearch()
    
    # Create a random query vector
    num_vectors = 1
    dimension = 1000
    vector = np.random.rand(num_vectors, dimension).astype('float32')
    
    print("Query vector shape:", vector.shape)
    
    # Perform a similarity search using the query vector
    results = faiss_search.search(query_vector=vector, top_k=3)
    
    print("Search results:", results)
