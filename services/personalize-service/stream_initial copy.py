import boto3
import botostubs
from botocore.exceptions import ClientError

pinpoint_client = boto3.client('pinpoint')  # type: botostubs.pinpoint
sts_client = boto3.client("sts")

account_id = sts_client.get_caller_identity()["Account"]

PINPOINT_ID = 'd5ab8b3e1788464cbc67948ab042fbcc'
KINESIS_STREAM_ARN = ''
EVENT_STREAM_IAM_ARN = ''

print('KINESIS_STREAM_ARN: ' + KINESIS_STREAM_ARN)
print('EVENT_STREAM_IAM_ARN ARN: ' + EVENT_STREAM_IAM_ARN)
print('Pinpoint event stream: creating')

try:
    response = pinpoint_client.put_event_stream(
        ApplicationId=PINPOINT_ID,
        WriteEventStream={
            'DestinationStreamArn': KINESIS_STREAM_ARN,
            'RoleArn': EVENT_STREAM_IAM_ARN
        }
    )
except ClientError as error:
    print(error)
