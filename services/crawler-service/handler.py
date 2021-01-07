import datetime
from logger import logger
from constant import SOURCE_SANOOK, SOURCE_THAIPBS, SOURCE_MATICHON, SOURCE_VOICETV

from handlers.handler_sanook import SanookHandler


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Cron function " + name + " ran at " + str(current_time))

    # dispatch
    source = event.get('source')
    url = event.get('url')
    category = event.get('category')
    print(f'crawl {source} {category} {url}')
    if(source == SOURCE_SANOOK):
        handler = SanookHandler(url=url, category=category)
    elif(source == SOURCE_THAIPBS):
        pass
    elif(source == SOURCE_MATICHON):
        pass
    elif(source == SOURCE_VOICETV):
        pass

    handler.run()
