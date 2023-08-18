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

    # Extract the columns from the DataFrame
    item_url = df.values[:, 0]
    item_image = df.values[:, 1]
    item_name = df.values[:, 2]
    item_price = df.values[:, 3]

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
                },
                "item_url": {"type": "text"},
                "item_image": {"type": "text"},
                "item_price": {"type": "text"},
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
            "_source": {
                'item_name': item_name[id],
                'item_url': item_url[id],
                'item_image': item_image[id],
                'item_price': item_price[id],
            }
        }
        for id in range(len(item_name))
    ]

    # Perform bulk indexing
    success, _ = helpers.bulk(elastic_search, actions, index=index_name)

    print(f"Indexed {success} documents")

if __name__ == "__main__":
    main()
