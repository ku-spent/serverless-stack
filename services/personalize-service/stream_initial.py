import boto3
import botostubs
import time

kinesisClient = boto3.client('kinesis') # type: botostubs.kinesis
pinpointClient = boto3.client('pinpoint') # type: botostubs.pinpoint

KINESIS_STREAM_NAME = 'spent-pinpoint-event'

response = kinesisClient.create_stream(
    StreamName=KINESIS_STREAM_NAME,
    ShardCount=1
)

print('Kinesis: creating')

while(True):
    time.sleep(2)
    response = kinesisClient.describe_stream(
        StreamName=KINESIS_STREAM_NAME,
        Limit=1,
    )
    status = response['StreamDescription']['StreamStatus']
    if(status == 'CREATING'):
        pass
    elif(status== 'ACTIVE'):
        print('Kinesis: active')
        break;
    else:
        raise Exception('Create kinesis stream error')

################
### Pinpoint ###
################
PINPOINT_ID = 'd5ab8b3e1788464cbc67948ab042fbcc'
KINESIS_STREAM_ARN = response['StreamDescription']['StreamARN']
EVENT_STREAM_IAM_ARN = 'arn:aws:iam::268400237357:role/spent-service-personalize-dev-PinpointKinesisRole-1GFPJ4XPFUUYS'
print('Kinesis ARN: ' + KINESIS_STREAM_ARN)
print('Pinpoint event stream: creating')
response = pinpointClient.put_event_stream(
    ApplicationId=PINPOINT_ID,
    WriteEventStream={
        'DestinationStreamArn': KINESIS_STREAM_ARN,
        'RoleArn': EVENT_STREAM_IAM_ARN
    }
)

print('CREATE SUCCESS!!')