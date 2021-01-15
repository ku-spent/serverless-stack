import re
import time
import string
from datetime import datetime, timedelta

import pytz
from bs4 import BeautifulSoup

SEVEN_HOURS = timedelta(hours=7)
SUMMARY_CLEAN = re.compile('<.*?>|\[.*?\]|&.*;')
whitelist_keys = ['title', 'summary', 'source']
table = str.maketrans(dict.fromkeys(string.punctuation))


def ensureHttps(url):
    return re.sub('http:', 'https:', url)


def get_pub_date(item):
    if('published_parsed' in item and item['published_parsed'] is not None):
        return time.strftime('%Y-%m-%dT%H:%M:%SZ', item['published_parsed'])
    else:
        return (datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ')


def local_datetime_to_utc(dt):
    local_time = pytz.timezone('Asia/Bangkok')
    local_dt = local_time.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def dict_with_keys(d, keys):
    return {x: d[x] for x in d if x in keys}


def clean_summary(text):
    return re.sub(SUMMARY_CLEAN, '', BeautifulSoup(text, features='lxml').get_text(strip=True)).strip()


def get_summary(item):
    if(item['source'] == 'สนุกดอทคอม'):
        return item['summary_detail']['value']
    else:
        return item['summary']


def get_image(item):
    if(item['source'] == 'มติชน'):
        if('media_thumbnail' in item):
            media = item['media_thumbnail']
            if(len(media) > 0):
                if('url' in media[0]):
                    return media[0]['url']
        return ''
    elif(item['source'] == 'Voice TV'):
        return item['href']
    elif((item['source'] == 'thaipbs') or (item['source'] == 'สนุกดอทคอม')):
        if(len(item['links']) > 1):
            image_obj = item['links'][1]
            if('image' not in image_obj['type']):
                return ''
            else:
                return image_obj['href']
    # base case
    return ''


label_to_index = {
    'ในประเทศ': 1,
    'บันเทิง': 2,
    'การเมือง': 3,
    'เศรษฐกิจ': 4,
    'กีฬา': 5,
    'อาชญากรรม': 6,
    'ไลฟ์สไตล์': 7,
    'ต่างประเทศ': 8,
    'เทคโนโลยี': 9,
    'สิ่งแวดล้อม': 10
}


index_to_lebel = {
    1: 'ในประเทศ',
    2: 'บันเทิง',
    3: 'การเมือง',
    4: 'เศรษฐกิจ',
    5: 'กีฬา',
    6: 'อาชญากรรม',
    7: 'ไลฟ์สไตล์',
    8: 'ต่างประเทศ',
    9: 'เทคโนโลยี',
    10: 'สิ่งแวดล้อม',
}
