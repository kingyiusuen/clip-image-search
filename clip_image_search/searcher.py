import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk


class Searcher:
    def __init__(self, region="us-east-1"):
        ssm = boto3.client("ssm", region_name=region)
        path = "/clip_image_search"
        es_endpoint = ssm.get_parameter(Name=f"{path}/es_endpoint")["Parameter"]["Value"]
        es_username = ssm.get_parameter(Name=f"{path}/es_master_username")["Parameter"]["Value"]
        es_password = ssm.get_parameter(Name=f"{path}/es_master_password", WithDecryption=True)["Parameter"]["Value"]

        self.client = Elasticsearch(
            hosts=[es_endpoint],
            http_auth=(es_username, es_password),
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            port=443,
        )
        self.index_name = "image"

    def create_index(self):
        knn_index = {
            "settings": {
                "index.knn": True,
            },
            "mappings": {
                "properties": {
                    "feature_vector": {
                        "type": "knn_vector",
                        "dimension": 512,
                    }
                }
            },
        }
        return self.client.indices.create(index=self.index_name, body=knn_index, ignore=400)

    def bulk_ingest(self, generate_data, chunk_size=128):
        return bulk(self.client, generate_data, chunk_size=chunk_size)

    def knn_search(self, query_features, k=10):
        body = {
            "size": k,
            "_source": {
                "exclude": ["feature_vector"],
            },
            "query": {
                "knn": {
                    "feature_vector": {
                        "vector": query_features,
                        "k": k,
                    }
                }
            },
        }
        return self.client.search(index=self.index_name, body=body)
