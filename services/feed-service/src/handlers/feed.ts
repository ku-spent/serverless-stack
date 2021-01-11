import * as AWS from 'aws-sdk'
import * as elasticsearch from 'elasticsearch'
import commonMiddleware from '../libs/commonMiddleware'
import { Handler } from 'aws-lambda'

const elasticClient = new elasticsearch.Client({
  host: process.env.ES_HOST,
  log: 'error',
  connectionClass: require('http-aws-es'),
})

const feed: Handler = async (event, context) => {
  const { from = 0, size = 5, query, queryField = '_' } = event?.queryStringParameters
  const _query = query
    ? { match: { [queryField]: { query } } }
    : {
        match_all: {},
      }

  const res = await elasticClient.search({
    index: process.env.ES_INDEX_RSS,
    sort: 'pubDate:desc',
    from: from,
    size: size,
    body: {
      query: _query,
    },
  })

  return {
    statusCode: 200,
    body: JSON.stringify({ data: res.hits }),
  }
}

export const handler = commonMiddleware(feed)
