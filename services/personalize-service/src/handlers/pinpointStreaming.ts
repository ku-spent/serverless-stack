import * as AWS from 'aws-sdk'

import { Handler } from 'aws-lambda'
import { PutEventsRequest } from 'aws-sdk/clients/cloudwatchevents'

console.log('Loading function')

const TRACKING_ID = process.env.TRACKING_ID || ''

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22' })

interface PersonalizeEvent {
  userId: string
  sessionId: string
  eventType: string
  sentAt: Date
  properties: string
}

const formatPayload = async () => {}

const putEventPersonalized = async (event: PersonalizeEvent) => {
  const { userId, sessionId, sentAt, eventType, properties } = event
  const params = {
    trackingId: TRACKING_ID,
    userId,
    sessionId,
    eventList: [
      {
        sentAt,
        eventType,
        properties,
      },
    ],
  }
  // const timestamp = Math.floor(e.data.timestamp_unixtime_ms / 1000);
  const res = await personalizedEvent.putEvents(params).promise()
  return res
}

const pintpointStreaming: Handler = async (event, context) => {
  event.Records.forEach(function (record) {
    // Kinesis data is base64 encoded so decode here
    var payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii')
    console.log('Decoded payload:', payload)
  })
}

export const handler = pintpointStreaming
