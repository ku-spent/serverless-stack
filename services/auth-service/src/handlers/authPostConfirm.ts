import { SNS_NEW_USER_TOPIC } from './config'
import { Handler } from 'aws-lambda'
import * as AWS from 'aws-sdk'
import { v4 as uuidv4 } from 'uuid'

// const cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' })
// const COGNITO_USERPOOL_ID = process.env.COGNITO_USERPOOL_ID || ''
const dynamoDb = new AWS.DynamoDB.DocumentClient()

const snsClient = new AWS.SNS({ apiVersion: '2010-03-31' })

const table = process.env.USER_TABLE_NAME || ''

console.log('Initial Auth post confirm trigger')

export const handler: Handler = async (event, context, callback) => {
  // const { sub, name, picture, email } = event.request.userAttributes
  console.log(event.request.userAttributes)

  const payload = { payload: event.request.userAttributes }
  const params = {
    Message: JSON.stringify(payload) /* required */,
    TopicArn: SNS_NEW_USER_TOPIC,
  }
  const res = await snsClient.publish(params).promise()
  console.log(JSON.stringify(res))
  callback(null, event)
}

// cognitoidentityserviceprovider.listGroups(params, function (err, data) {
//   if (err) console.log(err, err.stack)
//   // an error occurred
//   else if (data) {
//     console.log('Groups list:')
//     data.Groups?.map((groups) => {
//       console.log(groups.GroupName)
//     })

//     data.Groups?.map((groupEntity) => {
//       const params = {
//         GroupName: groupEntity.GroupName || '',
//         UserPoolId: COGNITO_USERPOOL_ID,
//       }
//       cognitoidentityserviceprovider.listUsersInGroup(params, function (err1, data1) {
//         if (err1) console.log(err1, err1.stack)
//         // an error occurred
//         else {
//           console.log(`${groupEntity.GroupName} has ${data1.Users?.length} users`)

//           data1.Users?.map((userEntity) => {
//             console.log(userEntity.Username)
//           })
//         }
//       })
//     })
//   }
// })
