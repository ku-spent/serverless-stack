from constant import GOOGLE_ES_INDEX, WEB_ES_INDEX
import datetime
from json import dumps, loads
import json
from logger import logger
from helper.elasticsearch import es


def run(event, context):
    current_time = datetime.datetime.now().time()
    logger.info(f'event: {dumps(event)}')
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    # dispatch
    try:
        records = [json.loads(record['body']) for record in event['Records']]
        print(len(records))
        for record in records:
            index = record['index']
            if(len(index) > 0):
                es.index(index=index, id=record['hash'], body=record['payload'])
            else:
                raise Exception('Invalid index')

        return 'Complete send payloads service'

    except Exception as e:
        print(e)

    finally:
        print('Complete crawler service')
