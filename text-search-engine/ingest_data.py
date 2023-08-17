import pandas as pd
from elasticsearch import Elasticsearch, helpers

def main():
    """
    This script reads data from a CSV file and indexes it into an Elasticsearch index.
    It demonstrates bulk indexing of data with specified mappings.
    """
    
    # Connect to Elasticsearch
    elastic_search = Elasticsearch("http://localhost:9200")

    # Read data from a CSV file into a Pandas DataFrame
    df = pd.read_csv("./data/data.csv", header=None)

    # Extract the column with item names from the DataFrame
    item_name_data = df.values[:, 2]

    index_name = 'text_search_index'

    # Define index mappings (optional but recommended)
    index_mappings = {
        "mappings": {
            "properties": {
                "item_name": {
                    "type": "text",
                    "fields": {
                        "suggest": {
                            "type": "completion"
                        }
                    }
                }
            }
        }
    }

    # Create the index with the defined mappings
    elastic_search.indices.create(index=index_name, body=index_mappings, ignore=400)  # ignore 400 means to ignore "Index Already Exists" errors

    # Prepare actions for bulk indexing
    actions = [
        {
            "_index": index_name,
            "_id": id,
            "_source": {'item_name': value}
        }
        for id, value in enumerate(item_name_data)
    ]

    # Perform bulk indexing
    success, _ = helpers.bulk(elastic_search, actions, index=index_name)

    print(f"Indexed {success} documents")

if __name__ == "__main__":
    main()
