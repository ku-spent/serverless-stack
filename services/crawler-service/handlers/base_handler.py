import json
import requests
import threading
from uuid import uuid4
from abc import ABC, abstractmethod
from requests.adapters import HTTPAdapter
from requests.models import HTTPError
from requests.packages.urllib3.util.retry import Retry

from constant import BASE_MAP_CATEGORY, BYPASS_CACHE, ES_PUBLISH, LOCAL, SNS_ARN, WEB_ES_INDEX
from helper.elasticsearch import es, index
from handlers.pre_processing import clean_summary, dict_with_keys, ensureHttps

import feedparser
from dict_hash import sha256
import boto3

HOURS_24 = 24 * 60 * 60

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

# sqs = boto3.client('sqs')
sns = boto3.client('sns')

def deleteSoupElement(element):
    if(isinstance(element, list)):
        for e in element:
            if(e):
                e.extract()
    elif(element):
        if(element):
            element.extract()


class BaseHandler(ABC, threading.Thread):
    payloads = []

    def __init__(self, url='', category='', additional_category_map={}):
        threading.Thread.__init__(self)
        super().__init__()
        self.es = es
        self.url = url
        self.category = category
        self.category_map = {**BASE_MAP_CATEGORY, **additional_category_map}
        dynamoDB = boto3.resource('dynamodb')

        # dynamoDB = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        self.newsUrlTable = dynamoDB.Table('NewsUrl')
        # self.cache = redis.Redis(connection_pool=pool)

    @abstractmethod
    def parse_news_link():
        pass

    @abstractmethod
    def pre_process():
        pass

    @abstractmethod
    def run():
        pass

    def pre_process(self, data):
        payload = {}
        payload['id'] = str(uuid4())
        payload['source'] = self.source
        payload['pubDate'] = data['pubDate']
        payload['url'] = ensureHttps(data['url'])
        payload['image'] = ensureHttps(data['image'])
        payload['title'] = data['title'].strip()
        payload['summary'] = clean_summary(data['summary'])
        payload['category'] = self.normalize_category(data['category'])
        payload['tags'] = data.get('tags', [])
        payload['raw_html_content'] = data['raw_html_content']
        return payload

    def normalize_category(self, category):
        if(self.category is not None):
            return self.category
        else:
            return self.category_map.get(category, LOCAL)

    def set_cache_link(self, link):
        if(BYPASS_CACHE):
            return
        self.newsUrlTable.put_item(
            Item={
                'url': link
            }
        )
        # self.cache.setex(link, HOURS_24, "True")

    def get_cache_link(self, link):
        if(BYPASS_CACHE):
            return None
        response = self.newsUrlTable.get_item(
            Key={
                'url': link
            }
        )
        return response.get('Item')
        # return self.cache.get(link)

    def get_raw_html(self, url):
        text = ''
        try:
            response = requests_retry_session().get(url, timeout=30, headers=headers)
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

    def hash_payload(self, payload):
        # keys = {'source', 'url', 'image', 'title', 'summary', 'category'}
        keys = {'url'}
        return sha256(dict_with_keys(payload, keys))

    def parse_url(self, url):
        feed = feedparser.parse(url)
        links = feed.entries
        if(len(links) > 0):
            return links
        return []

    def _format_bulk_body(self, entries, hash_func):
        body = []
        entries = [e for e in entries if e]
        for entry in entries:
            hash_value = hash_func(entry)
            keys = {'id', 'source', 'pubDate', 'url', 'image', 'title', 'summary', 'category', 'tags', 'raw_html_content'}
            payload = dict_with_keys(entry, keys)
            body.append({'index': {'_id': hash_value}})
            body.append(payload)
        return body

    def bulk_publish(self, entries, hash_func):
        hash_func = hash_func if hash_func is not None else self._hash_payload
        if(len(entries) > 0):
            body = self._format_bulk_body(entries, hash_func)
            for e in body:
                BaseHandler.payloads.append(e)
            # with open("test.txt", "w") as f:
            #     for item in body:
            #         f.write("%s\n" % item)
            # self.es.bulk(index=index, doc_type='_doc', body=body)
        print(f'Published successfully. {self.source} {self.url} total: {len(entries)} entries')

    def publish(self, payload, hash_func):
        hash_func = hash_func if hash_func is not None else self._hash_payload
        hash_value = hash_func(payload)
        keys = {'id', 'source', 'pubDate', 'url', 'image', 'title', 'summary', 'category', 'tags', 'raw_html_content'}
        body = {'index': WEB_ES_INDEX, 'hash': hash_value, 'payload': dict_with_keys(payload, keys)}
        # local dev
        if(ES_PUBLISH):
            es.index(index=index, id=body['hash'], body=body['payload'])
        else:
            response = sns.publish(TopicArn=SNS_ARN, Message=json.dumps(body), MessageAttributes={'crawlType': {'DataType': 'String', 'StringValue': 'news'}})
            return response['MessageId']


def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
