import * as AWS from 'aws-sdk'

import { Handler, Context, SQSEvent } from 'aws-lambda'
import PersonalizeEvents, { ItemList, PutItemsRequest } from 'aws-sdk/clients/personalizeevents'
import { PERSONALIZE_DATASET_ITEM_ARN } from '../config'

console.log('Loading function')

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22' })

interface Message {
  index: string
  hash: string
  payload: any
}

interface News {
  id: string
  source: string
  pubDate: string
  url: string
  image: string
  title: string
  summary: string
  category: string
  tags: string[]
  raw_html_content: string
}

const putItemsEvent = async (newsList: News[]) => {
  const items: ItemList = newsList.map((news) => ({
    itemId: news.id,
    properties: ({
      category: news.category,
      tags: news.tags.join('|'),
      source: news.source,
      creationTimestamp: Math.floor(Date.parse(news.pubDate) / 1000),
    } as any) as PersonalizeEvents.Types.ItemProperties,
  }))

  const event: PutItemsRequest = { datasetArn: PERSONALIZE_DATASET_ITEM_ARN, items }
  console.log(event)
  const res = await personalizedEvent.putItems(event).promise()
  return res
}

export const handler: Handler = async (event: SQSEvent, context: Context) => {
  const messages: Message[] = event.Records.map(({ body }) => JSON.parse(body))
    .map(({ Message }) => JSON.parse(Message))
    .filter(({ index }) => index.length > 0)

  if (messages.length > 10) {
    throw new Error('message length must less or equal 10.')
  }

  // console.log(messages)

  const newsList: News[] = messages.map((message) => message.payload)

  const res = await putItemsEvent(newsList)
  console.log(res)
  console.log('Completed')
  return res
}
