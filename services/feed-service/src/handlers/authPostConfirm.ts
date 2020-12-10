import { Handler } from 'aws-lambda'
import * as AWS from 'aws-sdk'

const cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider({ apiVersion: '2016-04-18' })
const COGNITO_USERPOOL_ID = process.env.COGNITO_USERPOOL_ID || ''
const params = {
  UserPoolId: COGNITO_USERPOOL_ID,
}

cognitoidentityserviceprovider.listGroups(params, function (err, data) {
  if (err) console.log(err, err.stack)
  // an error occurred
  else if (data) {
    console.log('Groups list:')
    data.Groups?.map((groups) => {
      console.log(groups.GroupName)
    })

    data.Groups?.map((groupEntity) => {
      const params = {
        GroupName: groupEntity.GroupName || '',
        UserPoolId: COGNITO_USERPOOL_ID,
      }
      cognitoidentityserviceprovider.listUsersInGroup(params, function (err1, data1) {
        if (err1) console.log(err1, err1.stack)
        // an error occurred
        else {
          console.log(`${groupEntity.GroupName} has ${data1.Users?.length} users`)

          data1.Users?.map((userEntity) => {
            console.log(userEntity.Username)
          })
        }
      })
    })
  }
})

export const handler: Handler = async (event, context) => {}
