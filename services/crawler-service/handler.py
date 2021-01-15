import datetime
from handlers.handler_beartai import BeartaiHandler
from handlers.handler_matichon import MatichonHandler
from handlers.handler_voicetv import VoiceTVHandler
from logger import logger
from constant import SOURCES, SOURCE_BEARTAI, SOURCE_SANOOK, SOURCE_MATICHON, SOURCE_VOICETV

from handlers.handler_sanook import SanookHandler


def build_handlers(Handler, Source):
    return [Handler(url=source['url'], category=source['category']) for source in Source]


def run(event, context):
    current_time = datetime.datetime.now().time()
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    # dispatch
    try:
        source = event.get('source')
        print(f'Start send payloads: {source}')

        handlers = []

        if(source == SOURCE_SANOOK):
            handlers = build_handlers(SanookHandler, SOURCES[SOURCE_SANOOK])
        elif(source == SOURCE_MATICHON):
            handlers = build_handlers(MatichonHandler, SOURCES[SOURCE_MATICHON])
        elif(source == SOURCE_VOICETV):
            handlers = build_handlers(VoiceTVHandler, SOURCES[SOURCE_VOICETV])
        elif(source == SOURCE_BEARTAI):
            handlers = build_handlers(BeartaiHandler, SOURCES[SOURCE_BEARTAI])

        for handler in handlers:
            handler.start()
        for handler in handlers:
            handler.join()

        if(len(handlers) > 0):
            payloads = handlers[0].payloads
        else:
            payloads = []

        return {'payloads': payloads}

    except Exception as e:
        raise str(e)
    finally:
        print('Complete crawler service')
