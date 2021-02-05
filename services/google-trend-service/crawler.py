import datetime
from json import dumps
import json
from logger import logger
from bs4 import BeautifulSoup

from helper import get_raw_html, es_client
from constant import EXTERNAL_TRENDS_ES_INDEX

SOURCE = 'thairath'


def handler(event, context):
    current_time = datetime.datetime.now().time()
    logger.info(f'event: {dumps(event)}')
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    try:
        raw_html = get_raw_html('https://www.thairath.co.th/tags/trending')
        soup = BeautifulSoup(raw_html, 'html.parser')
        tags = soup.find('main').find('div').find_all('div', recursive=False)[2].find_all('div')[5].find_all('a')

        trends = [tag.get_text() for tag in tags]
        now = datetime.datetime.utcnow().isoformat() + '+00:00'
        payload = {'source': SOURCE, 'trends': trends, 'createdAt': now}

        res = es_client.index(index=EXTERNAL_TRENDS_ES_INDEX, body=payload)
        print(json.dumps(res))
        return res

    except Exception as e:
        raise e
    finally:
        print('Complete external trends crawler service')
