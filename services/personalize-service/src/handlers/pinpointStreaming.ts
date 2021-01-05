import * as AWS from 'aws-sdk'

import { Handler } from 'aws-lambda'

console.log('Loading function')

const pintpointStreaming: Handler = async (event, context) => {
  event.Records.forEach(function (record) {
    // Kinesis data is base64 encoded so decode here
    var payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii')
    console.log('Decoded payload:', payload)
  })
}

export const handler = pintpointStreaming
