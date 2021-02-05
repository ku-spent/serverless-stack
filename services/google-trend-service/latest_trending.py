from constant import EXTERNAL_TRENDS_ES_INDEX
import datetime
from logger import logger
from json import dumps
from helper import es_client


def handler(event, context):
    current_time = datetime.datetime.now().time()
    logger.info(f'event: {dumps(event)}')
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    body = {
        "size": 1,
        "sort": {"createdAt": "desc"},
        "query": {
            "match_all": {}
        }
    }

    res = es_client.search(index=EXTERNAL_TRENDS_ES_INDEX, body=body)
    return res['hits']['hits'][0]['_source']
