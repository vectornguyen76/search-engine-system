from src.faiss_search.ingest_data import FaissIngest
from src.utils import LOGGER


def main():
    """
    Main function to perform QdrantIngest data ingestion.
    """
    # Create an instance of FaissIngest
    faiss_ingest = FaissIngest()

    if faiss_ingest.check_index_exists():
        LOGGER.info("Index in Faiss already exists!")
    else:
        LOGGER.info("Create Index in Faiss!")

        # Create and save the Faiss index
        faiss_ingest.create_index()


if __name__ == "__main__":
    main()
