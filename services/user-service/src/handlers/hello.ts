import * as AWS from 'aws-sdk'

import { Handler } from 'aws-lambda'
import commonMiddleware from '../libs/commonMiddleware'

const userPoolId = process.env.USERPOOL_ID || ''

const hello: Handler = async (event, context) => {
  const userId = event?.requestContext?.authorizer?.principalId
  console.log(userId)
  const cognito = new AWS.CognitoIdentityServiceProvider()
  const listUsersResponse = await cognito
    .listUsers({
      UserPoolId: userPoolId,
      Filter: `sub = "${userId}"`,
      Limit: 1,
    })
    .promise()
  return {
    statusCode: 200,
    body: JSON.stringify({ message: listUsersResponse.Users }),
  }
}

export const handler = commonMiddleware(hello)
