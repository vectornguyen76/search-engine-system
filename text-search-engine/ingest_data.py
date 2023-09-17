from elasticsearch import Elasticsearch, helpers
from config import settings
import pandas as pd

def main():
    """
    This script reads data from a CSV file and indexes it into an Elasticsearch index.
    It demonstrates bulk indexing of data with specified mappings.
    """
    
    # Connect to Elasticsearch
    elastic_search = Elasticsearch(settings.ELASTICSEARCH_HOST)

    # Read data from a CSV file into a Pandas DataFrame
    df = pd.read_csv("./data/data.csv")

    # Extract the columns from the DataFrame
    item_path = df['item_path']
    item_image = df['item_image']
    item_name = df['item_name']
    fixed_item_price = df['fixed_item_price']
    sale_item_price = df['sale_item_price']
    sales_number = df['sales_number']
    shop_path = df['shop_path']
    shop_name = df['shop_name']
        
    index_name = 'text_search_index'

    # Define index mappings (optional but recommended)
    index_mappings = {
        "settings": {
            "index": {
            "analysis": {
                "filter": {},
                "analyzer": {
                "keyword_analyzer": {
                    "filter": [
                    "lowercase",
                    "asciifolding",
                    "trim"
                    ],
                    "char_filter": [],
                    "type": "custom",
                    "tokenizer": "keyword"
                },
                "edge_ngram_analyzer": {
                    "filter": [
                    "lowercase"
                    ],
                    "tokenizer": "edge_ngram_tokenizer"
                },
                "edge_ngram_search_analyzer": {
                    "tokenizer": "lowercase"
                }
                },
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 5,
                        "token_chars": ["letter"]
                    }
                }
            }
            }
        },
        "mappings": {
            "properties": {
                "item_name": {
                    "type": "text",
                    "fields": {
                        "keywordstring": {
                            "type": "text",
                            "analyzer": "keyword_analyzer"
                        },
                        "edgengram": {
                            "type": "text",
                            "analyzer": "edge_ngram_analyzer",
                            "search_analyzer": "edge_ngram_search_analyzer"
                        },
                        "completion": {
                            "type": "completion"
                        }
                    },
                    "analyzer": "standard"
                },
                
                "item_path": {"type": "text"},
                "item_image": {"type": "text"},
                "fixed_item_price": {"type": "integer"},
                "sale_item_price": {"type": "integer"},
                "sales_number": {"type": "integer"},
                "shop_path": {"type": "text"},
                "shop_name": {"type": "text"},
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
                'item_path': item_path[id],
                'item_image': item_image[id],
                'fixed_item_price': fixed_item_price[id],
                'sale_item_price': sale_item_price[id],
                'sales_number': sales_number[id],
                'shop_path': shop_path[id],
                'shop_name': shop_name[id],
            }
        }
        for id in range(len(item_name))
    ]

    # Perform bulk indexing
    success, _ = helpers.bulk(elastic_search, actions, index=index_name)

    print(f"Indexed {success} documents")

if __name__ == "__main__":
    main()
