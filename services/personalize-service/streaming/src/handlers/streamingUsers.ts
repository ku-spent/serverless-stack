import { PERSONALIZE_DATASET_USER_ARN } from '../config'
import * as AWS from 'aws-sdk'

import { Handler, Context, SQSEvent } from 'aws-lambda'
import PersonalizeEvents, { PutItemsRequest, PutUsersRequest, UserList } from 'aws-sdk/clients/personalizeevents'

console.log('Loading function')

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22' })

interface Message {
  index: string
  hash: string
  payload: any
}

interface User {
  sub: string
  identities: string
  email_verified: string
  name: string
  'cognito:user_status': string
  phone_number_verified: string
  picture: string
  email: string
}

const putUsersEvent = async (userList: User[]) => {
  const users: UserList = userList.map((user) => ({
    userId: user.sub,
    properties: ({
      age: 20,
      gender: 'M',
    } as any) as PersonalizeEvents.Types.UserProperties,
  }))

  const event: PutUsersRequest = { datasetArn: PERSONALIZE_DATASET_USER_ARN, users }
  console.log(event)
  const res = await personalizedEvent.putUsers(event).promise()
  return res
}

export const handler: Handler = async (event: SQSEvent, context: Context) => {
  const messages: Message[] = event.Records.map(({ body }) => JSON.parse(body)).map(({ Message }) =>
    JSON.parse(Message)
  )

  if (messages.length > 10) {
    throw new Error('message length must less or equal 10.')
  }

  console.log(messages)

  const newsList: User[] = messages.map((message) => message.payload)

  const res = await putUsersEvent(newsList)
  console.log(res)
  console.log('Completed')
  return res
}
