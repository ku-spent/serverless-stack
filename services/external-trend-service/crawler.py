import datetime
from get_trends import get_trends
from json import dumps
from logger import logger
from helper import es_client
from constant import EXTERNAL_TRENDS_ES_INDEX


def handler(event, context):
    current_time = datetime.datetime.now().time()
    logger.info(f'event: {dumps(event)}')
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    try:
        trends, source = get_trends()
        now = datetime.datetime.utcnow().isoformat() + '+00:00'
        payload = {'source': source, 'trends': trends, 'createdAt': now}

        res = es_client.index(index=EXTERNAL_TRENDS_ES_INDEX, body=payload)
        print(dumps(res))
        return res

    except Exception as e:
        raise e
    finally:
        print('Complete external trends crawler service')
