import re
import time
import traceback
from datetime import datetime

from bs4 import BeautifulSoup

from logger import logger
from constant import CRAWL_DELAY, LOCAL, SOURCE_SANOOK
from handlers.base_handler import BaseHandler
from handlers.pre_processing import local_datetime_to_utc

ADDITIONAL_CATEGORY = {
    'ภูมิภาค': LOCAL,
}


class SanookHandler(BaseHandler):
    def __init__(self, url='', category=''):
        super().__init__(url, category, ADDITIONAL_CATEGORY)
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
        try:
            data = {}
            raw_html = self.get_raw_html(link)
            soup = BeautifulSoup(raw_html, 'html.parser')
            content_tag = soup.find(id='EntryReader_0')
            # ไม่เอาเพราะไม่ใช่เนื้อหาข่าว
            content_ul_tag = content_tag.find_all('ul')
            if(content_ul_tag):
                for ul_tag in content_ul_tag:
                    ul_tag.extract()
            data['raw_html_content'] = str(content_tag)
            data['tags'] = [tag.get_text() for tag in soup.find_all(class_='TagItem')]
            data['image'] = soup.find('div', class_='thumbnail').find('img')['src']
            data['pubDate'] = local_datetime_to_utc(datetime.strptime(soup.find('time')['datetime'], '%Y-%m-%d %H:%M'))
            data['category'] = soup.find(class_='SidebarWidget').find('div', class_='header').find('p').find('span').get_text()
            return data
        except Exception:
            traceback.print_exc()
            logger.info("Exception has occured", exc_info=1)
            return None

    def parse_url(self, url):
        items = []
        raw_html = self.get_raw_html(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        news_list = soup.find_all(class_='PostListWithDetail')
        for news in news_list:
            try:
                title = news.find(class_='gb-post-standard-title').get_text()
                link = news.find(class_='gb-post-standard-title').find('a')['href']
                summary = news.find(class_='description').get_text()
                items.append({'title': title, 'summary': summary, 'link': re.sub('^(//)', 'https://', link)})
            except Exception:
                traceback.print_exc()
                logger.info("Exception has occured", exc_info=1)
        return items

    def normalize(self, item, data):
        payload = {}
        payload['source'] = self.source
        payload['pubDate'] = data['pubDate']
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
