from elasticsearch import Elasticsearch
import ssl
from eunjeon import Mecab


ctx = ssl.create_default_context()
ctx.load_verify_locations("C:/Users/cjstk/Desktop/elasticsearch-8.1.0/cert1/http_ca.crt")

es = Elasticsearch("https://elastic:sw1594311@localhost:9200", ssl_context=ctx)

index = "dailynews"
body = {
    "query" : {
        "match" : {
            "date" : "2022.04.04"
        }
    }
}

result = es.search(index=index, body = body)
#print(result['hits']['hits'])
tag = Mecab()
