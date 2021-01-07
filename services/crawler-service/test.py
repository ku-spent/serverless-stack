from constant import SOURCE_SANOOK
# from handlers.handler_sanook import SanookHandler
import feedparser
import redis

rss = 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.index.xml'

HOURS_24 = 24 * 60 * 60


def test(url):
    feed = feedparser.parse(url)
    newsList = feed.entries
    if(len(newsList) > 0):
        return newsList, newsList[0]['link']
    return None, None


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
cache = redis.Redis(connection_pool=pool)
cache.setex('https://www.sanook.com/news/8329894/', HOURS_24, "True")
print(cache.get('https://www.sanook.com/news/8329894/'))
# handler = SanookHandler(url='http://rssfeeds.sanook.com/rss/feeds/sanook/news.politic.xml', category='การเมือง')
# handler.run()