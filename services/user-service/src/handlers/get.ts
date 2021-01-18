import { dynamodb } from './../libs/dynamodb'
import { APIGatewayProxyEvent, Handler, Context } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'
import { USER_TABLE_NAME } from '../config'

interface LambdaEvent {
  pathParameters: {
    id: string
  }
}

const get: Handler = async (event: APIGatewayProxyEvent & LambdaEvent, context: Context) => {
  const { id } = event.pathParameters
  const user = await dynamodb.get({ TableName: USER_TABLE_NAME, Key: { id } }).promise()
  return {
    statusCode: 200,
    body: JSON.stringify({ data: user }),
  }
}

export const handler = commonMiddleware(get)
