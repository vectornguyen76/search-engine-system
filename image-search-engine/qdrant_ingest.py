from src.qdrant_search.ingest_data import QdrantIngest
from src.utils import LOGGER



def main():
    """
    Main function to perform QdrantIngest data ingestion.
    """
    qdrant_ingest = QdrantIngest()

    try:
        response = qdrant_ingest.check_collection()
        if response.result.status == 1:
            LOGGER.info("Collection already exists!")
    except Exception as e:
        LOGGER.info(f"Error checking collection: {e}")

        LOGGER.info("Create collection!")
        response = qdrant_ingest.create_collection()
        LOGGER.info(response)

        qdrant_ingest.add_points()

if __name__ == "__main__":
    main()
