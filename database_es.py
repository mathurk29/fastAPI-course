import os
from ssl import create_default_context

from elasticsearch import Elasticsearch

context = create_default_context(
    cafile=os.path.join(os.getcwd(), 'http_ca.crt'))
es_username = 'elastic'
es_password = 'qKYIzMP1BXYlxOiHRD6V'
wsl_elasticsearch = Elasticsearch(
    ['https://elastic:qKYIzMP1BXYlxOiHRD6V@localhost:9200'], ssl_context=context)

print(f'ES connected: {wsl_elasticsearch.ping()}')
