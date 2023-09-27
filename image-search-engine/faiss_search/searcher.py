import faiss
import numpy as np
import pandas as pd
from config import settings


class FaissSearch:
    """
    A class for performing similarity search using the Faiss library.

    This class provides functionality to perform similarity search using a pre-built Faiss index.

    Attributes:
        index (faiss.Index): The Faiss index used for search.
        item_path (np.ndarray): URLs of items in the dataset.
        item_image (np.ndarray): Image paths of items in the dataset.
        item_name (np.ndarray): Names of items in the dataset.
        fixed_item_price (np.ndarray): Fixed prices of items in the dataset.
        sale_item_price (np.ndarray): Sale prices of items in the dataset.
        sales_number (np.ndarray): Sales numbers of items in the dataset.
        shop_path (np.ndarray): Paths of shops where items are sold.
        shop_name (np.ndarray): Names of shops where items are sold.
    """

    def __init__(self):
        """
        Initializes the FaissSearch class.

        This class provides functionality to perform similarity search using the Faiss library.
        """
        # Load the dataset
        data = pd.read_csv(settings.DATA_PATH)

        # Read the Faiss index
        self.index = faiss.read_index(settings.INDEX_PATH)

        # Extract attributes from the dataset
        self.item_path = data["item_path"]
        self.item_image = data["item_image"]
        self.item_name = data["item_name"]
        self.fixed_item_price = data["fixed_item_price"]
        self.sale_item_price = data["sale_item_price"]
        self.sales_number = data["sales_number"]
        self.shop_path = data["shop_path"]
        self.shop_name = data["shop_name"]

    def search(self, query_vector, top_k=settings.TOP_K):
        """
        Performs a similarity search using the provided query vector.

        Args:
        - query_vector (np.ndarray): The query vector for similarity search.
        - top_k (int, optional): The number of nearest neighbors to retrieve. Default is specified in settings.

        Returns:
        - list: A list of dictionaries containing search results, including item information.
        """
        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:
            sale_rate = 1 - (self.sale_item_price[idx] / self.fixed_item_price[idx])
            results.append(
                {
                    "item_path": self.item_path[idx],
                    "item_image": self.item_image[idx],
                    "item_name": self.item_name[idx],
                    "fixed_item_price": self.fixed_item_price[idx],
                    "sale_item_price": self.sale_item_price[idx],
                    "sale_rate": sale_rate,
                    "sales_number": self.sales_number[idx],
                    "shop_path": self.shop_path[idx],
                    "shop_name": self.shop_name[idx],
                }
            )

        return results


if __name__ == "__main__":
    # Instantiate the FaissSearch class
    faiss_search = FaissSearch()

    # Create a random query vector
    num_vectors = 1
    dimension = 1000
    vector = np.random.rand(num_vectors, dimension).astype("float32")

    print("Query vector shape:", vector.shape)

    # Perform a similarity search using the query vector
    results = faiss_search.search(query_vector=vector, top_k=3)

    print("Search results:", results)
