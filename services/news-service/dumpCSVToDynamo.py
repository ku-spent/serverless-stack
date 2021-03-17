import boto3
import csv

dynamodb = boto3.resource('dynamodb')

tableName = 'News'
csv_file_name = 'items_raw.csv'
batch_size = 9
batch = []


def write_to_dynamo(rows):
    # print(rows)
    try:
        table = dynamodb.Table(tableName)
    except:
        print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

    try:
        with table.batch_writer() as batch:
            for i in range(len(rows)):
                row = rows[i]
                row['tags'] = row['tags'].split('|')
                batch.put_item(Item=rows[i])
    except Exception as e:
        print(e)
        print("Error executing batch_writer")


with open(csv_file_name, newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    i = 0
    for row in csv_reader:
        i = i + 1
        if(i % batch_size == 0):
            print(i)
        if(len(batch) >= batch_size):
            write_to_dynamo(batch)
            batch.clear()

        batch.append(row)
        # break

    if len(batch) > 0:
        write_to_dynamo(batch)
