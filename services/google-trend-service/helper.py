import boto3
import requests
from requests.models import HTTPError
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

from constant import ELASTICSEACH_HOST


service = 'es'
credentials = boto3.Session().get_credentials()
host = ELASTICSEACH_HOST
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, 'ap-southeast-1', service, session_token=credentials.token)

es_client = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30, max_retries=10, retry_on_timeout=True
)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}


def get_raw_html(url):
    text = ''
    try:
        response = requests.get(url, timeout=30, headers=headers)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        text = response.content
    finally:
        return text
