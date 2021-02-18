import * as AWS from 'aws-sdk'

import { Handler, KinesisStreamEvent, Context, KinesisStreamRecord } from 'aws-lambda'
import { Payload } from '../types'
import { PutEventsRequest } from 'aws-sdk/clients/personalizeevents'
import { PERSONALIZE_TRACKING_ID } from '../config'

console.log('Loading function')

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22' })

const formatPayload = async (payload: string) => {
  const jsonPayload: Payload = JSON.parse(payload)
  const event: PutEventsRequest = {
    trackingId: PERSONALIZE_TRACKING_ID,
    userId: jsonPayload.attributes.user_id,
    sessionId: jsonPayload.session.session_id,
    eventList: [
      {
        sentAt: new Date(jsonPayload.event_timestamp),
        eventType: jsonPayload.event_type,
        properties: JSON.stringify({ itemId: jsonPayload.attributes.news_id }),
      },
    ],
  }
  return event
}

const putInteractionEvent = async (record: KinesisStreamRecord) => {
  const payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii')
  console.log('Decoded payload:', payload)

  const formattedEvent = await formatPayload(payload)
  const res = await personalizedEvent.putEvents(formattedEvent).promise()
  return res
}

export const handler: Handler = async (event: KinesisStreamEvent, context: Context) => {
  const res = await Promise.all(event.Records.map((record) => putInteractionEvent(record)))
  return res
}
