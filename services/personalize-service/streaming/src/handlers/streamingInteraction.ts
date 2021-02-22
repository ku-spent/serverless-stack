import * as AWS from 'aws-sdk'

import { Handler, KinesisStreamEvent, Context, KinesisStreamRecord } from 'aws-lambda'
import { Payload } from '../types'
import PersonalizeEvents, { PutEventsRequest } from 'aws-sdk/clients/personalizeevents'
import { PERSONALIZE_TRACKING_ID } from '../config'

console.log('Loading function')

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22' })

const formatPayload = async (payload: Payload) => {
  console.log(payload)
  const event: PutEventsRequest = {
    trackingId: PERSONALIZE_TRACKING_ID,
    userId: payload.attributes.user_id,
    sessionId: payload.session.session_id,
    eventList: [
      {
        sentAt: new Date(payload.event_timestamp),
        eventType: payload.event_type,
        properties: ({ itemId: payload.attributes.news_id } as any) as PersonalizeEvents.Types.EventPropertiesJSON,
      },
    ],
  }
  console.log(event)
  return event
}

const putInteractionEvent = async (record: KinesisStreamRecord) => {
  const payload = Buffer.from(record.kinesis.data, 'base64').toString('ascii')
  console.log('Decoded payload:', payload)

  const jsonPayload: Payload = JSON.parse(payload)

  if (jsonPayload.event_type === '_test.event_stream') {
    return null
  }

  const formattedEvent = await formatPayload(jsonPayload)
  const res = await personalizedEvent.putEvents(formattedEvent).promise()
  return res
}

export const handler: Handler = async (event: KinesisStreamEvent, context: Context) => {
  const res = await Promise.all(event.Records.map((record) => putInteractionEvent(record)))
  console.log(res)
  // return res
}
