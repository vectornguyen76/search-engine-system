from src.elastic_search.ingest_data import ElasticSeachIngest
from src.utils import LOGGER

def main():
    """
    Main function to perform Elasticsearch data ingestion.
    """
    es_ingest = ElasticSeachIngest()
    if es_ingest.check_index_exists():
        LOGGER.info("Index in Elastic Search already exists!")
    else:
        LOGGER.info("Create Index in Elastic Search!")
        es_ingest.create_index()
        es_ingest.indexing_batch_document()


if __name__ == "__main__":
    main()
