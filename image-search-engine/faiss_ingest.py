from src.faiss_search.ingest_data import FaissIngest
from src.utils import LOGGER

# Create an instance of FaissIngest
faiss_ingest = FaissIngest()

if faiss_ingest.check_index_exists():
    LOGGER.info("Faiss index already exists!")
else:
    # Create and save the Faiss index
    faiss_ingest.create_index()
