import { APIGatewayProxyEvent, Handler, Context } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'

interface LambdaEvent {
  pathParameters: {
    id: string
  }
}

const get: Handler = async (event: APIGatewayProxyEvent & LambdaEvent, context: Context) => {
  const { id } = event.pathParameters

  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'ok' }),
  }
}

export const handler = commonMiddleware(get)
