import datetime
from handlers.handler_matichon import MatichonHandler
from handlers.handler_voicetv import VoiceTVHandler
from logger import logger
from constant import SOURCES, SOURCE_SANOOK, SOURCE_THAIPBS, SOURCE_MATICHON, SOURCE_VOICETV

from handlers.handler_sanook import SanookHandler


def run(event, context):
    current_time = datetime.datetime.now().time()
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    # dispatch
    source = event.get('source')
    print(f'Start crawl source: {source}')
    handlers = []

    if(source == SOURCE_SANOOK):
        handlers = [SanookHandler(url=source['url'], category=source['category']) for source in SOURCES[SOURCE_SANOOK]]
    elif(source == SOURCE_THAIPBS):
        pass
    elif(source == SOURCE_MATICHON):
        handlers = [MatichonHandler(url=source['url'], category=source['category']) for source in SOURCES[SOURCE_MATICHON]]
    elif(source == SOURCE_VOICETV):
        handlers = [VoiceTVHandler(url=source['url'], category=source['category']) for source in SOURCES[SOURCE_VOICETV]]

    for handler in handlers:
        handler.start()
    for handler in handlers:
        handler.join()

    print('Complete crawler service')
