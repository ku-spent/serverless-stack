from constant import GOOGLE_ES_INDEX, QUEUE_URL
import datetime
import boto3
from json import dumps
from logger import logger
from pytrends.request import TrendReq
from dict_hash import sha256

sqs = boto3.client('sqs')


def run(event, context):
    current_time = datetime.datetime.now().time()
    logger.info(f'event: {dumps(event)}')
    try:
        name = context.function_name
        logger.info("Cron function " + name + " ran at " + str(current_time))
    except Exception:
        pass

    try:
        pytrends = TrendReq(hl='th-TH', geo='TH')
        trends = pytrends.trending_searches(pn='thailand')
        formated_trends = [data[0] for data in list(trends.to_numpy())]
        now = datetime.datetime.utcnow().isoformat() + '+00:00'
        payload = {'trends': formated_trends, 'createdAt': now}
        hash_value = sha256(payload)

        body = {'index': GOOGLE_ES_INDEX, 'hash': hash_value, 'payload': payload}
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=dumps(body)
        )
        print(response['MessageId'])
        return response['MessageId']

    except Exception as e:
        raise e
    finally:
        print('Complete google crawler service')
