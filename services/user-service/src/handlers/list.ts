import { dynamodb } from './../libs/dynamodb'
import { APIGatewayProxyEvent, Handler, Context } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'
import { USER_TABLE_NAME } from '../config'

interface LambdaEvent {}

const get: Handler = async (event: APIGatewayProxyEvent, context: Context) => {
  const users = await dynamodb.scan({ TableName: USER_TABLE_NAME }).promise()
  return {
    statusCode: 200,
    body: JSON.stringify({ data: users }),
  }
}

export const handler = commonMiddleware(get)
