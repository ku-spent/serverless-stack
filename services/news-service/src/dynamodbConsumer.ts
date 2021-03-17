import { elasticClient } from './libs/elasticsearch'
import { Handler, Context, SQSEvent } from 'aws-lambda'
import { DynamoDB } from 'aws-sdk'
import { PutItemInputAttributeMap } from 'aws-sdk/clients/dynamodb'

interface Message {
  index: string
  hash: string
  payload: any
}

const dynamodb = new DynamoDB({ apiVersion: '2012-08-10', region: 'ap-southeast-1' })

export const handler: Handler = async (event: SQSEvent, context: Context) => {
  const messages: Message[] = event.Records.map(({ body }) => JSON.parse(body))
    .map(({ Message }) => JSON.parse(Message))
    .filter(({ index }) => index.length > 0)

  const res = await Promise.all(
    messages.map(({ hash, payload }) => {
      const { url, title, image, summary, source, pubDate, category, raw_html_content, tags } = payload
      console.log(payload)
      const item: PutItemInputAttributeMap = {
        id: { S: hash },
        url: { S: url },
        title: { S: title },
        summary: { S: summary },
        source: { S: source },
        pubDate: { S: pubDate },
        category: { S: category },
        image: { S: image },
        raw_html_content: { S: raw_html_content },
        ...(tags.length > 0 && { tags: { SS: tags } }),
      }
      return dynamodb.putItem({ Item: item, TableName: 'News' }).promise()
    })
  )

  console.log(res)
  return res
}
