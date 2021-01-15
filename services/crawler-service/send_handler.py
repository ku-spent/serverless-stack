import datetime
from json import dumps, loads
import json
from logger import logger
from helper.elasticsearch import es, index


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
            es.index(index=index, id=record['_id'], body=record['payload'])

        return 'Complete send payloads service'

    except Exception as e:
        raise str(e)

    finally:
        print('Complete crawler service')
