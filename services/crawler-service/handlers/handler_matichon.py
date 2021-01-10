import traceback
import time

import feedparser
from bs4 import BeautifulSoup

from constant import SOURCE_MATICHON, SOURCE_VOICETV
from logger import logger
from handlers.base_handler import BaseHandler

ADDITIONAL_CATEGORY = {
}


class MatichonHandler(BaseHandler):
    def __init__(self, url='', category=''):
        super().__init__(url, category, ADDITIONAL_CATEGORY)
        self.url = url
        self.category = category
        self.source = SOURCE_MATICHON

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
            content = soup.find(class_='td-post-content')
            image_tag = content.find(class_='td-post-featured-image')
            data['image'] = image_tag.find('a')['href']
            if(image_tag):
                image_tag.extract()
            data['raw_html_content'] = str(content.find_all('p'))
            data['tags'] = []
            tags_elem = soup.find(class_='td-post-source-tags')
            if(tags_elem):
                for tag in tags_elem.find_all('li'):
                    data['tags'].append(tag.get_text())
            data['tags'] = [tag for tag in data['tags'] if tag != 'แท็ก']
            data['category'] = soup.find(class_='ud-post-category-title').get_text()
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
                pubDate = time.strftime('%Y-%m-%dT%H:%M:%SZ', news['published_parsed'])
                items.append({'title': title, 'summary': title, 'link': link, 'pubDate': pubDate})
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
            self.bulk_publish(entries)

        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
