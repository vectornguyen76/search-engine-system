import pandas as pd
from config import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk
from tqdm import tqdm
from src.utils import LOGGER

class ElasticSeachIngest:
    """
    A class for ingesting data into Elasticsearch.

    Attributes:
        elastic_search (Elasticsearch): An Elasticsearch client.
        index_name (str): The name of the Elasticsearch index to create.
        data (DataFrame): The data to be ingested as a Pandas DataFrame.
        number_of_docs (int): The number of documents in the dataset.
    """

    def __init__(self):
        """
        Initialize the ElasticSeachIngest instance.
        """
        self.elastic_search = Elasticsearch(settings.ELASTICSEARCH_HOST)
        self.index_name = settings.INDEX_NAME
        self.data = pd.read_csv(settings.DATA_PATH)
        self.number_of_docs = len(self.data.index)

    def create_index(self):
        """
        Create an Elasticsearch index with specified mappings.
        """
        index_mappings = {
            "settings": {
                "index": {
                    "analysis": {
                        "filter": {},
                        "analyzer": {
                            "keyword_analyzer": {
                                "filter": ["lowercase", "asciifolding", "trim"],
                                "char_filter": [],
                                "type": "custom",
                                "tokenizer": "keyword",
                            },
                            "edge_ngram_analyzer": {
                                "filter": ["lowercase"],
                                "tokenizer": "edge_ngram_tokenizer",
                            },
                            "edge_ngram_search_analyzer": {"tokenizer": "lowercase"},
                        },
                        "tokenizer": {
                            "edge_ngram_tokenizer": {
                                "type": "edge_ngram",
                                "min_gram": 2,
                                "max_gram": 5,
                                "token_chars": ["letter"],
                            }
                        },
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
                                "analyzer": "keyword_analyzer",
                            },
                            "edgengram": {
                                "type": "text",
                                "analyzer": "edge_ngram_analyzer",
                                "search_analyzer": "edge_ngram_search_analyzer",
                            },
                            "completion": {"type": "completion"},
                        },
                        "analyzer": "standard",
                    },
                    "item_path": {"type": "text"},
                    "item_image": {"type": "text"},
                    "fixed_item_price": {"type": "integer"},
                    "sale_item_price": {"type": "integer"},
                    "sale_rate": {"type": "float"},
                    "sales_number": {"type": "integer"},
                    "shop_path": {"type": "text"},
                    "shop_name": {"type": "text"},
                }
            },
        }

        # Create the index with the defined mappings
        self.elastic_search.indices.create(
            index=self.index_name, body=index_mappings, ignore=400
        )  # ignore 400 means to ignore "Index Already Exists" errors

    def generate_actions(self):
        """
        Generate actions (documents) to be indexed in Elasticsearch.
        """
        for index, row in self.data.iterrows():
            doc = {
                "_id": index,
                "_source": {
                    "item_name": row["item_name"],
                    "item_path": row["item_path"],
                    "item_image": row["item_image"],
                    "fixed_item_price": row["fixed_item_price"],
                    "sale_item_price": row["sale_item_price"],
                    "sale_rate": 1 - (row["sale_item_price"] / row["fixed_item_price"]),
                    "sales_number": row["sales_number"],
                    "shop_path": row["shop_path"],
                    "shop_name": row["shop_name"],
                },
            }
            yield doc

    def indexing_document(self):
        """
        Index documents in Elasticsearch using streaming_bulk.
        """
        progress = tqdm(unit="docs", total=self.number_of_docs)
        successes = 0
        for success, _ in streaming_bulk(
            client=self.elastic_search,
            index=self.index_name,
            actions=self.generate_actions(),
        ):
            progress.update(1)
            successes += success

        LOGGER.info(f"Indexed {successes}/{self.number_of_docs} documents")

    def indexing_batch_document(self):
        """
        Index documents in Elasticsearch in batches.
        """
        batch_size = 5000

        num_batches = (self.number_of_docs + batch_size - 1) // batch_size
        successes = 0
        for i in tqdm(range(num_batches)):
            # Split into batches
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, self.number_of_docs)

            actions = []
            for idx in range(start_idx, end_idx):
                sale_rate = 1 - (
                    self.data["sale_item_price"][idx]
                    / self.data["fixed_item_price"][idx]
                )
                actions.append(
                    {
                        "_id": idx,
                        "_source": {
                            "item_name": self.data["item_name"][idx],
                            "item_path": self.data["item_path"][idx],
                            "item_image": self.data["item_image"][idx],
                            "fixed_item_price": self.data["fixed_item_price"][idx],
                            "sale_item_price": self.data["sale_item_price"][idx],
                            "sale_rate": sale_rate,
                            "sales_number": self.data["sales_number"][idx],
                            "shop_path": self.data["shop_path"][idx],
                            "shop_name": self.data["shop_name"][idx],
                        },
                    }
                )
            # Perform bulk indexing
            success, _ = bulk(self.elastic_search, actions, index=self.index_name)
            successes += success

        LOGGER.info(f"Indexed {successes}/{self.number_of_docs} documents")

    def check_index_exists(self):
        """Check index name exists"""
        return self.elastic_search.indices.exists(index=self.index_name)
