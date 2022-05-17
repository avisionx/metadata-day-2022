from elasticsearch import Elasticsearch
from data import MOCK_RANDOM_DATA

# Configs
ELASTIC_URL = "https://localhost:9200"
PATH_ELASTIC_CERTS = "~/Downloads/elasticsearch-8.2.0/config/certs/http_ca.crt"
ELASTIC_PASSWORD = "YOUR_PASSWORD_HERE"

# Index Name
INDEX = "database-index"


def init_elastic_client():
    # initialize client
    client = Elasticsearch(
        ELASTIC_URL,
        ca_certs=PATH_ELASTIC_CERTS,
        basic_auth=("elastic", ELASTIC_PASSWORD),
    )
    # Put data
    for document in MOCK_RANDOM_DATA:
        client.index(index=INDEX, id=document["id"], document=document)
    return client


def elastic_search(client, field_regex=""):
    # Try searching for field_regex
    resp = client.search(
        index=INDEX,
        query={
            "query_string": {
                "query": "*",
                "fields": [field_regex],
            }
        },
    )
    unique_db_hits = set()
    for hit in resp["hits"]["hits"]:
        unique_db_hits.add(hit["_source"]["database"])

    separator = "-" * 10 + " Searching " + field_regex + " " + "-" * 10
    print(separator)

    print("No. Database with this field:", len(unique_db_hits))
    print("List of Database:", unique_db_hits)
    print("-" * len(separator))


if __name__ == "__main__":
    client = init_elastic_client()
    # Match for bitcoin_address field
    elastic_search(client, field_regex="*coin*")
    # Match for ip_address field
    elastic_search(client, field_regex="*ip_*")
