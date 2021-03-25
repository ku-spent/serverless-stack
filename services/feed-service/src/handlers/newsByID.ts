import AWS from 'aws-sdk'
import { APIGatewayEvent, Handler } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'
import { GetItemInput, QueryInput, ScanInput } from 'aws-sdk/clients/dynamodb'

interface Event extends APIGatewayEvent {
  pathParameters: {
    id: string
  }
}

const dynamodb = new AWS.DynamoDB({ apiVersion: '2012-08-10' })

const news: Handler = async (event: Event, context) => {
  const { id } = event.pathParameters

  if (id == '')
    return {
      statusCode: 400,
    }

  const params: GetItemInput = {
    TableName: 'News2',
    Key: {
      id: { S: id },
    },
  }

  const res = await dynamodb.getItem(params).promise()
  const data = res.Item ? AWS.DynamoDB.Converter.unmarshall(res.Item) : null
  return {
    statusCode: 200,
    body: JSON.stringify({ data }),
  }
}

export const handler = commonMiddleware(news)
