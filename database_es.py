import os
from ssl import create_default_context

from elasticsearch import Elasticsearch

context = create_default_context(
    cafile=os.path.join(os.getcwd(), "http_ca.crt")
)
es_username = "elastic"
es_password = os.environ["ELASTIC_PASSWORD"]
if es_password is None:
    raise ValueError("env variable ELASTIC_PASSWORD is not set")
wsl_elasticsearch = Elasticsearch(
    [f"https://{es_username}:{es_password}@localhost:9200"], ssl_context=context
)

print(f"ES connected: {wsl_elasticsearch.ping()}")
