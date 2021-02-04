import { elasticClient } from './libs/elasticsearch'
import { Handler, Context, SQSEvent } from 'aws-lambda'
import { ES_INDEX } from './constant'

interface Message {
  index: string
  hash: string
  payload: any
}

export const handler: Handler = async (event: SQSEvent, context: Context) => {
  const messages: Message[] = event.Records.map(({ body }) => JSON.parse(body))
    .map(({ Message }) => JSON.parse(Message))
    .filter(({ index }) => index.length > 0)

  const res = await Promise.all(
    messages.map(({ hash, payload }) => elasticClient.index({ id: hash, type: '_doc', index: ES_INDEX, body: payload }))
  )

  const createdResult = res
    .filter(({ result }) => result === 'created')
    .map(({ _id, result }) => ({
      _id,
      result,
    }))

  console.log(createdResult)
  return createdResult
}
