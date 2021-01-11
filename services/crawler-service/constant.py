import os

SOURCE_SANOOK = os.getenv('SOURCE_SANOOK', 'สนุกดอทคอม')

SOURCE_THAIPBS = os.getenv('SOURCE_THAIPBS', 'thaipbs')

SOURCE_MATICHON = os.getenv('SOURCE_MATICHON', 'มติชน')

SOURCE_VOICETV = os.getenv('SOURCE_VOICETV', 'Voice TV')

POLITICS = 'การเมือง'
ECONOMIC = 'เศรษฐกิจ'
INTERNATIONAL = 'ต่างประเทศ'
CRIME = 'อาชญากรรม'
SPORT = 'กีฬา'
LOCAL = 'ในประเทศ'
ENTERTAINMENT = 'บันเทิง'
LIFESTYLE = 'ไลฟ์สไตล์'
ENVIRONMENT = 'สิ่งแวดล้อม'
TECHNOLOGY = 'เทคโนโลยี'
SOCIAL = 'สังคม'
LIFE = 'คุณภาพชีวิต'
EDUCATION = 'การศึกษา'

SOURCES = {
    SOURCE_SANOOK: [
        {'category': None, 'url': 'https://www.sanook.com/news/archive/'},
        {'category': ENTERTAINMENT, 'url': 'https://www.sanook.com/news/archive/entertain/'},
        {'category': ECONOMIC, 'url': 'https://www.sanook.com/money/archive/'},
        {'category': TECHNOLOGY, 'url': 'https://www.sanook.com/hitech/archive/'},
        {'category': SPORT, 'url': 'https://www.sanook.com/sport/archive/'},
        {'category': LIFESTYLE, 'url': 'https://www.sanook.com/travel/archive/'},
    ],
    SOURCE_THAIPBS: [
    ],
    SOURCE_MATICHON: [
        {'category': POLITICS, 'url': 'https://www.matichon.co.th/politics/feed'},
        {'category': ECONOMIC, 'url': 'https://www.matichon.co.th/economy/feed'},
        {'category': LOCAL, 'url': 'https://www.matichon.co.th/local/feed'},
        {'category': INTERNATIONAL, 'url': 'https://www.matichon.co.th/foreign/feed'},
        {'category': EDUCATION, 'url': 'https://www.matichon.co.th/education/feed'},
        {'category': LIFESTYLE, 'url': 'https://www.matichon.co.th/lifestyle/feed'},
        {'category': ENTERTAINMENT, 'url': 'https://www.matichon.co.th/entertainment/feed'},
        {'category': SPORT, 'url': 'https://www.matichon.co.th/sport/sport-inter/feed'},
    ],
    SOURCE_VOICETV: [
        {'category': None, 'url': 'https://voicetv.co.th/rss'}
    ],
}

BASE_MAP_CATEGORY = {
    POLITICS: POLITICS,
    ECONOMIC: ECONOMIC,
    INTERNATIONAL: INTERNATIONAL,
    CRIME: CRIME,
    SPORT: SPORT,
    LOCAL: LOCAL,
    ENTERTAINMENT: ENTERTAINMENT,
    LIFESTYLE: LIFESTYLE,
    ENVIRONMENT: ENVIRONMENT,
    TECHNOLOGY: TECHNOLOGY,
    SOCIAL: SOCIAL,
    LIFE: LIFE,
}

ELASTIC_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
ELASTICSEACH_HOST = os.getenv('ELASTICSEACH_HOST', 'search-spent-eoyffh53pimfhjrbhiyf5gscqa.ap-southeast-1.es.amazonaws.com')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
ES_INDEX = os.getenv('ES_INDEX', 'rss-feed-3')

# TEXT_CLASSIFY_ENDPOINT = os.getenv('TEXT_CLASSIFY_ENDPOINT')
# NEWS_TABLE_NAME = os.getenv('NEWS_TABLE_NAME')
# APPSYNC_COGNITO_USERNAME = os.getenv('COGNITO_ADMIN_USERNAME')
# APPSYNC_COGNITO_PASSWORD = os.getenv('COGNITO_ADMIN_PASSWORD')
# APPSYNC_COGNITO_CLIENTID = "5tkbsrfe13o1vav6nflunq3pkm"
# APPSYNC_COGNITO_USERPOOL_ID = "ap-southeast-1_5BfiF60iL"
# APPSYNC_API_ENDPOINT_URL = 'https://quxwa5rc3vgglbri3rujvmgmry.appsync-api.ap-southeast-1.amazonaws.com/graphql'
