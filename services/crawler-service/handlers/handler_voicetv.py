import time
import traceback
from datetime import datetime

import feedparser
from bs4 import BeautifulSoup

from constant import SOURCE_VOICETV
from logger import logger
from handlers.base_handler import BaseHandler

ADDITIONAL_CATEGORY = {
}


class VoiceTVHandler(BaseHandler):
    def __init__(self, url='', category=''):
        super().__init__(url, category, ADDITIONAL_CATEGORY)
        self.url = url
        self.category = category
        self.source = SOURCE_VOICETV

    def get_image_from_item(self, item):
        image = ''
        if(len(item['links']) > 1):
            image_obj = item['links'][1]
            if('image' in image_obj['type']):
                image = image_obj['href']
        return image

    def parse_news_link(self, link):
        try:
            data = {}
            raw_html = self.get_raw_html(link)
            soup = BeautifulSoup(raw_html, 'html.parser')
            data['summary'] = soup.find(class_='excerpt').get_text()
            data['raw_html_content'] = str(soup.find(class_='content-description'))
            data['tags'] = []
            for tag in soup.find_all(class_='details'):
                tag = tag.find('a')
                unwated_tag = tag.find('span')
                if(unwated_tag):
                    unwated_tag.extract()
                data['tags'].append(tag.get_text())
            data['category'] = soup.find(class_='topic').get_text()
            pubDate = soup.find(class_='date last').get_text().split('Last update')[1][:-2].strip()
            data['pubDate'] = datetime.strptime(pubDate, '%b %d, %Y %H:%M').isoformat()
            return data
        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
            return None

    def parse_url(self, url):
        items = []
        feed = feedparser.parse(url)
        news_list = feed.entries
        for news in news_list:
            try:
                title = news['title']
                link = news['link']
                image = news['href']
                items.append({'title': title, 'link': link, 'image': image})
            except Exception:
                traceback.print_exc()
                logger.info("Exception has occured", exc_info=1)
        return items

    def normalize(self, item, data):
        payload = {}
        payload['source'] = self.source
        payload['pubDate'] = data['pubDate']
        payload['url'] = item['link']
        payload['image'] = item['image']
        payload['title'] = item['title']
        payload['summary'] = data['summary']
        payload['category'] = data['category']
        payload['tags'] = data.get('tags', [])
        payload['raw_html_content'] = data['raw_html_content']

        return payload

    def run(self):
        try:
            print(f'Start crawl {self.category} from {self.url}')
            items = self.parse_url(self.url)
            entries = []
            for item in items:
                if(item is None):
                    continue
                link = item['link']

                # visited
                cache = self.get_cache_link(link)
                if(cache is not None):
                    continue
                # not visited
                else:
                    self.set_cache_link(link)

                time.sleep(1)
                data = self.parse_news_link(link)
                if(data is None):
                    continue
                data = self.normalize(item, data)
                data = self.pre_process(data)
                print(f'Data {data["source"]} {data["category"]} {data["url"]}')
                entries.append(data)
            self.bulk_publish(entries, self.hash_payload)

        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
