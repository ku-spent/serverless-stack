import boto3
import botostubs
import time
import sys

kinesisClient = boto3.client('kinesis') # type: botostubs.kinesis

KINESIS_STREAM_NAME = 'spent-pinpoint-event'

print('Kinesis: deleting')

try:
    response = kinesisClient.delete_stream(
        StreamName=KINESIS_STREAM_NAME,
        EnforceConsumerDeletion=True
    )
except:
    e = sys.exc_info()[0]
    if(e.__name__ == 'ResourceNotFoundException'):
        print('Delete success')
    else:
        print('Delete error')


while(True):
    try:
        time.sleep(2)
        response = kinesisClient.describe_stream(
            StreamName=KINESIS_STREAM_NAME,
            Limit=1,
        )
    except:
        e = sys.exc_info()[0]
        if(e.__name__ == 'ResourceNotFoundException'):
            print('Delete success')
        else:
            print('Delete error')
        break;