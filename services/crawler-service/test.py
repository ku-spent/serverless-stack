# from web_crawler.handler import run
from handler import run
from constant import SOURCE_BEARTAI, SOURCE_HACKERNOON, SOURCE_MATICHON, SOURCE_SANOOK, SOURCE_VOICETV
# from handlers.handler_sanook import SanookHandler
import feedparser
import boto3

rss = 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.index.xml'

HOURS_24 = 24 * 60 * 60


def test(url):
    feed = feedparser.parse(url)
    newsList = feed.entries
    if(len(newsList) > 0):
        return newsList, newsList[0]['link']
    return None, None

# ES_PUBLISH=True BYPASS_CACHE=True python3 test.py
run({'source': SOURCE_BEARTAI}, {})
# run({'source': SOURCE_VOICETV}, {})
# run({'source': SOURCE_MATICHON}, {})
# run({'source': SOURCE_BEARTAI}, {})
# run({'source': SOURCE_HACKERNOON}, {})

# pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# cache = redis.Redis(connection_pool=pool)
# cache.setex('https://www.sanook.com/news/8329894/', HOURS_24, "True")
# print(cache.get('https://www.sanook.com/news/8329894/'))
# handler = SanookHandler(url='http://rssfeeds.sanook.com/rss/feeds/sanook/news.politic.xml', category='การเมือง')
# handler.run()

# For a Boto3 client.


# dynamoDB = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
# newsUrlTable = dynamoDB.Table('NewsUrl')
# newsUrlTable.put_item(
#     Item={
#         'url': 'janedoe'
#     }
# )
# print(newsUrlTable.get_item(
#     Key={
#         'url': 'janedoe',
#     }
# ).get('Item'))
