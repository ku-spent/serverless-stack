import { Handler } from 'aws-lambda'
import esb, { boolQuery, matchAllQuery, matchQuery, termQuery } from 'elastic-builder'
import commonMiddleware from '../libs/commonMiddleware'
import { esSearch } from '../libs/elasticsearch'

const news: Handler = async (event, context) => {
  const { from = 0, size = 5, query, queryField = '_' } = event?.queryStringParameters

  const body = esb
    .requestBodySearch()
    .query(query ? matchQuery(queryField, query) : matchAllQuery())
    .sort(esb.sort('pubDate', 'desc'))
    .from(from)
    .size(size)
    .toJSON()

  const res = await esSearch(body)

  return {
    statusCode: 200,
    body: JSON.stringify({ data: res.hits }),
  }
}

export const handler = commonMiddleware(news)
