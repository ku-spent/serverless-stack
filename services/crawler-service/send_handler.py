import datetime
from logger import logger
from helper.elasticsearch import es, index


def run(event, context, callback):
    current_time = datetime.datetime.now().time()
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    # dispatch
    try:
        payloads = event.payloads
        print(len(payloads))

        if(len(payloads) > 0):
            es.bulk(index=index, doc_type='_doc', body=payloads)
            print(f'sending {len(payloads)} items')

        callback(None, 'Complete send payloads service')

    except Exception as e:
        callback(str(e))
    finally:
        print()
