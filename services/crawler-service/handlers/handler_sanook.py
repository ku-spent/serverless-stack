import traceback
from uuid import uuid4
from datetime import datetime

from bs4 import BeautifulSoup

from logger import logger
from constant import SOURCE_SANOOK
from handlers.base_handler import BaseHandler
from handlers.pre_processing import clean_summary, ensureHttps, local_datetime_to_utc


class SanookHandler(BaseHandler):
    def __init__(self, url='', category=''):
        super().__init__()
        self.url = url
        self.category = category
        self.source = SOURCE_SANOOK

    def get_image_from_item(self, item):
        image = ''
        if(len(item['links']) > 1):
            image_obj = item['links'][1]
            if('image' in image_obj['type']):
                image = image_obj['href']
        return image

    def parse_news_link(self, link):
        data = {}
        raw_html = self.get_raw_html(link)
        soup = BeautifulSoup(raw_html, 'html.parser')
        data['raw_html_content'] = str(soup.find(id='EntryReader_0'))
        data['tags'] = [tag.get_text() for tag in soup.find_all(class_='TagItem')]
        data['pubDate'] = local_datetime_to_utc(datetime.strptime(soup.find('time')['datetime'], '%Y-%m-%d %H:%M'))
        return data

    def pre_process(self, item, data):
        payload = {}
        payload['id'] = str(uuid4())
        payload['source'] = self.source
        payload['pubDate'] = data['pubDate']
        payload['url'] = ensureHttps(item['link'])
        payload['image'] = ensureHttps(self.get_image_from_item(item))
        payload['title'] = item['title'].strip()
        payload['summary'] = clean_summary(item['summary_detail']['value'])
        payload['category'] = self.category
        payload['tags'] = data['tags']
        payload['raw_html_content'] = data['raw_html_content']
        return payload

    def run(self):
        try:
            items = self.parse_url(self.url)
            entries = []
            for item in items:
                if(item is None):
                    continue
                link = item['link']
                print(link)

                # visited
                cache = self.get_cache_link(link)
                if(cache is not None):
                    continue
                # not visited
                else:
                    self.set_cache_link(link)
                data = self.parse_news_link(link)
                data = self.pre_process(item, data)
                entries.append(data)
            self.bulk_publish(entries)
        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
