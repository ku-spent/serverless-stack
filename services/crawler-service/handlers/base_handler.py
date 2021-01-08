import requests
import threading
from abc import ABC, abstractmethod
from requests.adapters import HTTPAdapter
from requests.models import HTTPError
from requests.packages.urllib3.util.retry import Retry

from constant import BASE_MAP_CATEGORY, LOCAL, REDIS_HOST
from helper.elasticsearch import es, index
from handlers.pre_processing import dict_with_keys

import redis
import feedparser
from dict_hash import sha256

HOURS_24 = 24 * 60 * 60

ADDITIONAL_CATEGORY = {
    'ภูมิภาค': LOCAL,
}


class BaseHandler(ABC, threading.Thread):
    def __init__(self, url='', category='', additional_category_map={}):
        threading.Thread.__init__(self)
        super().__init__()
        self.es = es
        self.url = url
        self.category = category
        self.category_map = {**BASE_MAP_CATEGORY, **additional_category_map}
        pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=0)
        self.cache = redis.Redis(connection_pool=pool)

    @abstractmethod
    def parse_news_link():
        pass

    @abstractmethod
    def pre_process():
        pass

    @abstractmethod
    def run():
        pass

    def normalize_category(self, category):
        if(self.category is not None):
            return self.category
        else:
            return self.category_map.get(category, LOCAL)

    def set_cache_link(self, link):
        self.cache.setex(link, HOURS_24, "True")

    def get_cache_link(self, link):
        return self.cache.get(link)

    def get_raw_html(self, url):
        text = ''
        try:
            response = requests_retry_session().get(url, timeout=30)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            text = response.text
        finally:
            return text

    def _hash_payload(self, payload):
        keys = {'source', 'url', 'image', 'title', 'summary', 'category'}
        return sha256(dict_with_keys(payload, keys))

    def parse_url(self, url):
        feed = feedparser.parse(url)
        links = feed.entries
        if(len(links) > 0):
            return links
        return []

    def _format_bulk_body(self, entries):
        body = []
        for entry in entries:
            hash_value = self._hash_payload(entry)
            keys = {'id', 'source', 'pubDate', 'url', 'image', 'title', 'summary', 'category', 'tags', 'raw_html_content'}
            payload = dict_with_keys(entry, keys)
            body.append({'index': {'_id': hash_value}})
            body.append(payload)
        return body

    def bulk_publish(self, entries):
        if(len(entries) > 0):
            body = self._format_bulk_body(entries)
            # with open("test.txt", "a") as f:
            #     for item in body:
            #         f.write("%s\n" % item)
            self.es.bulk(index=index, doc_type='_doc', body=body)
        print(f'Published successfully. {self.source} {self.url} total: {len(entries)} entries')

    def publish(self, payload):
        hash_value = self.hash_payload(payload)
        keys = {'id', 'source', 'pubDate', 'url', 'image', 'title', 'summary', 'category', 'tags', 'raw_html_content'}
        self.es.index(index=index, id=hash_value, body=dict_with_keys(payload, keys))
        print('Message published successfully.', payload['url'])


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
