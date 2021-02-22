import boto3
import time
from botocore.exceptions import ClientError

sts_client = boto3.client("sts")
lambda_client = boto3.client('lambda')

account_id = sts_client.get_caller_identity()["Account"]

LAMBDA_NAME = 'spent-service-personalize-dev-streamingPersonalizeInteractions'
KINESIS_STREAM_ARN = f'arn:aws:kinesis:ap-southeast-1:{account_id}:stream/spent-pinpoint-event'
print(KINESIS_STREAM_ARN)
try:
    response = lambda_client.list_event_source_mappings(
        FunctionName=LAMBDA_NAME,
    )
    print(f'Deleting {len(response["EventSourceMappings"])}')
    for eventSource in response['EventSourceMappings']:
        response = lambda_client.delete_event_source_mapping(UUID=eventSource['UUID'])
except ClientError as error:
    print(error)

time.sleep(2)

try:
    response = lambda_client.create_event_source_mapping(
        EventSourceArn=KINESIS_STREAM_ARN,
        FunctionName=LAMBDA_NAME,
        Enabled=True,
        BatchSize=10,
        MaximumBatchingWindowInSeconds=10,
        StartingPosition='LATEST',
    )
    print(response)
except ClientError as error:
    print(error)
