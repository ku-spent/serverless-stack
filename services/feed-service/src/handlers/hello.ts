import { Handler } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'

const hello: Handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'hello' }),
  }
}

export const handler = commonMiddleware(hello)
