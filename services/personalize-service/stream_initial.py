import json
import boto3
import botostubs
import time
from botocore.exceptions import ClientError

kinesis_client = boto3.client('kinesis')  # type: botostubs.kinesis
pinpoint_client = boto3.client('pinpoint')  # type: botostubs.pinpoint
iam_client = boto3.client("iam")
sts_client = boto3.client("sts")

account_id = sts_client.get_caller_identity()["Account"]

KINESIS_STREAM_NAME = 'spent-pinpoint-event'

try:
    response = kinesis_client.create_stream(
        StreamName=KINESIS_STREAM_NAME,
        ShardCount=1
    )
except ClientError as error:
    print(error)


print('Kinesis: creating')

while(True):
    time.sleep(2)
    response = kinesis_client.describe_stream(
        StreamName=KINESIS_STREAM_NAME,
        Limit=1,
    )
    status = response['StreamDescription']['StreamStatus']
    if(status == 'CREATING'):
        pass
    elif(status == 'ACTIVE'):
        print('Kinesis: active')
        break
    else:
        raise Exception('Create kinesis stream error')


role_name = 'spentPinpointKinesisStream'
policy_name = role_name + 'Policy'

pinpoint_kinesis_stream_assume_role = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "pinpoint.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
# create role
try:
    create_role_res = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(pinpoint_kinesis_stream_assume_role),
        Description="This is a pinpoint role",
        Tags=[{"Key": "Owner", "Value": "spent-pinpoint"}],
    )
    print('create role success')
except ClientError as error:
    print(error)

pinpoint_kinesis_stream_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kinesis:PutRecords",
                "kinesis:DescribeStream"
            ],
            "Resource": [
                f"arn:aws:kinesis:ap-southeast-1:{account_id}:stream/{KINESIS_STREAM_NAME}"
            ],
            "Effect": "Allow"
        },
        # {
        #     "Action": [
        #         "kinesis:DescribeStream",
        #         "kinesis:DescribeStreamSummary",
        #         "kinesis:GetRecords",
        #         "kinesis:GetShardIterator",
        #         "kinesis:ListShards",
        #         "kinesis:ListStreams",
        #         "kinesis:SubscribeToShard"
        #     ],
        #     "Resource": [
        #         f"arn:aws:lambda:ap-southeast-1:{account_id}:function:spent-service-personalize-*"
        #     ],
        #     "Effect": "Allow"
        # }
    ]
}

# create policy
try:
    policy_res = iam_client.create_policy(
        PolicyName=policy_name, PolicyDocument=json.dumps(pinpoint_kinesis_stream_policy)
    )
    policy_arn = policy_res["Policy"]["Arn"]
    print('create policy success')
except ClientError as error:
    print(error.response["Error"]["Code"])
    if error.response["Error"]["Code"] == "EntityAlreadyExists":
        print("Policy already exists")
        policy_arn = "arn:aws:iam::" + account_id + ":policy/" + policy_name
else:
    print("Role could not be created...")

# attch role policy
try:
    policy_attach_res = iam_client.attach_role_policy(
        RoleName=role_name, PolicyArn=policy_arn
    )
    print('attach policy success')
except ClientError as error:
    print(error)


################
### Pinpoint ###
################
PINPOINT_ID = 'd5ab8b3e1788464cbc67948ab042fbcc'
KINESIS_STREAM_ARN = response['StreamDescription']['StreamARN']
EVENT_STREAM_IAM_ARN = iam_client.get_role(RoleName=role_name)["Role"]["Arn"]
# EVENT_STREAM_IAM_ARN = 'arn:aws:iam::268400237357:role/spent-service-personalize-dev-PinpointKinesisRole-1GFPJ4XPFUUYS'

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

response = kinesis_client.register_stream_consumer(
    StreamARN=KINESIS_STREAM_ARN,
    ConsumerName=KINESIS_STREAM_NAME + 'Consumer'
)


print('CREATE SUCCESS!!')
