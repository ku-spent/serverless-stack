import os

SOURCE_SANOOK = 'สนุกดอทคอม'

SOURCE_THAIPBS = 'thaipbs'

SOURCE_MATICHON = 'มติชน'

SOURCE_VOICETV = 'voiceTV'

SOURCES = {
    SOURCE_SANOOK: {'url': 'http://rssfeeds.sanook.com/rss/feeds/sanook/news.index.xml', 'name': 'สนุกดอทคอม'},
    SOURCE_THAIPBS: {'url': 'https://news.thaipbs.or.th/rss/news', 'name': 'thaipbs'},
    SOURCE_MATICHON: {'url': 'https://www.matichon.co.th/feed', 'name': 'มติชน'},
    SOURCE_VOICETV: {'url': 'https://voicetv.co.th/rss/breaking', 'name': 'Voice TV'},
    # {'url': 'https://www.prachachat.net/feed', 'name': 'ประชาชาติ'},
    # {'url': 'https://www.thairath.co.th/rss/news', 'name': 'ไทยรัฐ'},
}

ELASTIC_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
ELASTICSEACH_HOST = os.getenv('ELASTICSEACH_HOST', 'q1efoi7143.execute-api.ap-southeast-1.amazonaws.com')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# TEXT_CLASSIFY_ENDPOINT = os.getenv('TEXT_CLASSIFY_ENDPOINT')
# NEWS_TABLE_NAME = os.getenv('NEWS_TABLE_NAME')
# APPSYNC_COGNITO_USERNAME = os.getenv('COGNITO_ADMIN_USERNAME')
# APPSYNC_COGNITO_PASSWORD = os.getenv('COGNITO_ADMIN_PASSWORD')
# APPSYNC_COGNITO_CLIENTID = "5tkbsrfe13o1vav6nflunq3pkm"
# APPSYNC_COGNITO_USERPOOL_ID = "ap-southeast-1_5BfiF60iL"
# APPSYNC_API_ENDPOINT_URL = 'https://quxwa5rc3vgglbri3rujvmgmry.appsync-api.ap-southeast-1.amazonaws.com/graphql'
