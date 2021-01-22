import json
import time
import traceback

import feedparser
from bs4 import BeautifulSoup

from constant import CRAWL_DELAY, SOURCE_HACKERNOON
from logger import logger
from handlers.base_handler import BaseHandler, deleteSoupElement

ADDITIONAL_CATEGORY = {
}


class HackernoonHandler(BaseHandler):
    def __init__(self, url='', category=''):
        super().__init__(url, category, ADDITIONAL_CATEGORY)
        self.url = url
        self.category = category
        self.source = SOURCE_HACKERNOON

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
            content_tag = soup.select_one('div[class*="Container-"]')
            data['image'] = content_tag.find(class_='fullscreen').find('img')['src']
            deleteSoupElement(content_tag.find('h1'))
            deleteSoupElement(content_tag.select('div[class*="Reactions"]'))
            deleteSoupElement(content_tag.select_one('div[class*="StoryMeta"]'))
            deleteSoupElement(content_tag.find('div', class_='image-container'))
            deleteSoupElement(content_tag.select_one('div[class*="Profile"]'))
            deleteSoupElement(content_tag.find(class_='bottom-reactions'))
            deleteSoupElement(content_tag.find('footer'))
            deleteSoupElement(content_tag.find(class_='related-stories'))
            deleteSoupElement(content_tag.find('section'))
            deleteSoupElement(content_tag.select('div[class*="CallToAction"]'))
            data['raw_html_content'] = str(content_tag)
            return data
        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
            print(link)
            return None

    def parse_url(self, url):
        items = []
        feed = feedparser.parse(url)
        news_list = feed.entries
        for news in news_list:
            try:
                title = news['title']
                link = news['link']
                summary = news['summary']
                pubDate = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', news['published_parsed'])
                tags = [tag['term'] for tag in news['tags']]
                items.append({'title': title, 'link': link, 'summary': summary, 'pubDate': pubDate, 'tags': tags})
            except Exception:
                traceback.print_exc()
                logger.info("Exception has occured", exc_info=1)
        return items

    def normalize(self, item, data):
        payload = {}
        payload['source'] = self.source
        payload['pubDate'] = item['pubDate']
        payload['url'] = item['link']
        payload['image'] = data['image']
        payload['title'] = item['title']
        payload['summary'] = item['summary']
        payload['category'] = self.category
        payload['tags'] = item.get('tags', [])
        payload['raw_html_content'] = data['raw_html_content']

        return payload

    def run(self):
        try:
            print(f'Start crawl {self.category} from {self.url}')
            items = self.parse_url(self.url)
            for item in items:
                if(item is None):
                    continue
                link = item['link']

                # visited
                cache = self.get_cache_link(link)
                if(cache is not None):
                    continue

                time.sleep(CRAWL_DELAY)
                data = self.parse_news_link(link)
                if(data is None):
                    continue
                data = self.normalize(item, data)
                data = self.pre_process(data)
                print(f'Data {data["source"]} {data["category"]} {data["url"]}')
                self.publish(data, self.hash_payload)

                if(cache is None):
                    self.set_cache_link(link)

        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
