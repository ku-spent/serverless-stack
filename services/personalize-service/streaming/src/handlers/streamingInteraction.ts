import * as AWS from 'aws-sdk'

import { Handler, KinesisStreamEvent, Context, KinesisStreamRecord } from 'aws-lambda'
import { Payload } from '../types'
import PersonalizeEvents, { PutEventsRequest } from 'aws-sdk/clients/personalizeevents'
import { PERSONALIZE_TRACKING_ID } from '../config'

console.log('Loading function')

const allow_interaction = ['news_viewed', 'news_bookmarked', 'news_shared', 'news_liked']

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
  console.log(JSON.stringify(event))
  return event
}

const putInteractionEvent = async (record: KinesisStreamRecord) => {
  const payload = Buffer.from(record.kinesis.data, 'base64').toString('utf-8')
  console.log('Decoded payload:', payload)

  // const parsedUnicodeJson = utf8.encode(payload)

  const jsonPayload: Payload = JSON.parse(payload)

  if (!allow_interaction.includes(jsonPayload.event_type)) {
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
