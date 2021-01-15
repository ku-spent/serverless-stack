import datetime
from json import dumps
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
        payloads = event['payloads']
        print(len(payloads))

        if(len(payloads) > 0):
            es.bulk(index=index, doc_type='_doc', body=payloads)
            print(f'sending {len(payloads)} items')

        return 'Complete send payloads service'

    except Exception as e:
        raise str(e)

    finally:
        print('Complete crawler service')
