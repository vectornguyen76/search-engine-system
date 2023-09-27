from config import settings
from elasticsearch import Elasticsearch

# Create a connection to your Elasticsearch cluster
es = Elasticsearch(settings.ELASTICSEARCH_HOST)

index_name = settings.INDEX_NAME

# Delete the index
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted")
else:
    print(f"Index '{index_name}' does not exist")
