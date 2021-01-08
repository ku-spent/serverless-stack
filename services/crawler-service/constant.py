import os

SOURCE_SANOOK = os.getenv('SOURCE_SANOOK', 'สนุกดอทคอม')

SOURCE_THAIPBS = os.getenv('SOURCE_THAIPBS', 'thaipbs')

SOURCE_MATICHON = os.getenv('SOURCE_MATICHON', 'มติชน')

SOURCE_VOICETV = os.getenv('SOURCE_VOICETV', 'voiceTV')

SOURCES = {
    SOURCE_SANOOK: [
        {'category': 'การเมือง', 'url': 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.politic.xml'},
        {'category': 'อาชญากรรม', 'url': 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.crime.xml'},
        {'category': 'เศรษฐกิจ', 'url': 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.economic.xml'}
    ],
    SOURCE_THAIPBS: [],
    SOURCE_MATICHON: [],
    SOURCE_VOICETV: [],
}

ELASTIC_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
ELASTICSEACH_HOST = os.getenv('ELASTICSEACH_HOST', 'search-spent-eoyffh53pimfhjrbhiyf5gscqa.ap-southeast-1.es.amazonaws.com')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# TEXT_CLASSIFY_ENDPOINT = os.getenv('TEXT_CLASSIFY_ENDPOINT')
# NEWS_TABLE_NAME = os.getenv('NEWS_TABLE_NAME')
# APPSYNC_COGNITO_USERNAME = os.getenv('COGNITO_ADMIN_USERNAME')
# APPSYNC_COGNITO_PASSWORD = os.getenv('COGNITO_ADMIN_PASSWORD')
# APPSYNC_COGNITO_CLIENTID = "5tkbsrfe13o1vav6nflunq3pkm"
# APPSYNC_COGNITO_USERPOOL_ID = "ap-southeast-1_5BfiF60iL"
# APPSYNC_API_ENDPOINT_URL = 'https://quxwa5rc3vgglbri3rujvmgmry.appsync-api.ap-southeast-1.amazonaws.com/graphql'
