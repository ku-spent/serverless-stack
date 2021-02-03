import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

from constant import ELASTIC_REGION, ELASTICSEACH_HOST, ACCESS_KEY, SECRET_KEY, WEB_ES_INDEX


service = 'es'
index = WEB_ES_INDEX
credentials = boto3.Session().get_credentials()
host = ELASTICSEACH_HOST
awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, ELASTIC_REGION, service)
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, ELASTIC_REGION, service)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30, max_retries=10, retry_on_timeout=True
)

# es.indices.create(index=index, ignore=400)
