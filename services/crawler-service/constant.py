import os

SOURCE_SANOOK = os.getenv('SOURCE_SANOOK', 'สนุกดอทคอม')

SOURCE_THAIPBS = os.getenv('SOURCE_THAIPBS', 'thaipbs')

SOURCE_MATICHON = os.getenv('SOURCE_MATICHON', 'มติชน')

SOURCE_VOICETV = os.getenv('SOURCE_VOICETV', 'Voice TV')

SOURCE_BEARTAI = os.getenv('SOURCE_BEARTAI', 'beartai')

SOURCE_HACKERNOON = os.getenv('SOURCE_HACKERNOON', 'hackernoon')

CRAWL_DELAY = 0.8

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
MOVIE = 'ภาพยนตร์'
MUSIC = 'เพลง'
AI = 'ai'
DATA_SCIENCE = 'data-science'
WEB_DEVELOPMENT = 'web-development'
BIG_DATA = 'big-data'
MARKETING = 'marketing'
DL = 'deep-learning'
ML = 'machine-learning'
DS = 'data-science'
CYBER_SECURITY = 'cybersecurity'
BLOCKCHAIN = 'blockchain'
BITCOIN = 'bitcoin'
STARTUP = 'startups'
PROGRAMMING = 'programming'

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
    SOURCE_BEARTAI: [
        {'category': TECHNOLOGY, 'url': 'https://www.beartai.com/category/news'},
        {'category': MOVIE, 'url': 'https://www.beartai.com/category/lifestyle/movies'},
        {'category': MOVIE, 'url': 'https://www.beartai.com/category/lifestyle/tv-series'},
        {'category': MUSIC, 'url': 'https://www.beartai.com/category/lifestyle/music-lifestyle'},
        {'category': ENTERTAINMENT, 'url': 'https://www.beartai.com/category/lifestyle/entertainment'},
    ],
    SOURCE_HACKERNOON: [
        {'category': STARTUP, 'url': 'https://hackernoon.com/tagged/startups/feed'},
        {'category': MARKETING, 'url': 'https://hackernoon.com/tagged/marketing/feed'},
        {'category': DL, 'url': 'https://hackernoon.com/tagged/deep-learning/feed'},
        {'category': ML, 'url': 'https://hackernoon.com/tagged/machine-learning/feed'},
        {'category': DS, 'url': 'https://hackernoon.com/tagged/data-science/feed'},
        {'category': CYBER_SECURITY, 'url': 'https://hackernoon.com/tagged/cybersecurity/feed'},
        {'category': BIG_DATA, 'url': 'https://hackernoon.com/tagged/big-data/feed'},
        {'category': BLOCKCHAIN, 'url': 'https://hackernoon.com/tagged/blockchain/feed'},
        {'category': BITCOIN, 'url': 'https://hackernoon.com/tagged/bitcoin/feed'},
        {'category': WEB_DEVELOPMENT, 'url': 'https://hackernoon.com/tagged/web-development/feed'},
        {'category': AI, 'url': 'https://hackernoon.com/tagged/ai/feed'},
        {'category': PROGRAMMING, 'url': 'https://hackernoon.com/tagged/programming/feed'},
    ]
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
    EDUCATION: EDUCATION,
    MOVIE: MOVIE,
    MUSIC: MUSIC,
}

ELASTIC_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
ELASTICSEACH_HOST = os.getenv('ELASTICSEACH_HOST', 'search-spent-eoyffh53pimfhjrbhiyf5gscqa.ap-southeast-1.es.amazonaws.com')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
WEB_ES_INDEX = os.getenv('WEB_ES_INDEX', '')
GOOGLE_ES_INDEX = os.getenv('GOOGLE_ES_INDEX', '')
BYPASS_CACHE = bool(os.getenv('BYPASS_CACHE', False))
ES_PUBLISH = bool(os.getenv('ES_PUBLISH', False))
SNS_ARN = os.getenv('SNS_ARN', '')
