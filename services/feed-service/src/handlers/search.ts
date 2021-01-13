import { Handler } from 'aws-lambda'
import esb from 'elastic-builder'
import { esSearch } from '../libs/elasticsearch'
import commonMiddleware from '../libs/commonMiddleware'

const search: Handler = async (event, context) => {
  const { q, from = 0, size = 5 } = event?.queryStringParameters

  const requestBody = esb
    .requestBodySearch()
    .query(
      esb
        .functionScoreQuery()
        .query(esb.multiMatchQuery().query(q).fields(['title', 'summary']).operator('or'))
        .functions([
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-7d').lt('now')).weight(5),
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-1m').lt('now-7d')).weight(2),
          esb.decayScoreFunction().field('pubDate').origin('now').scale('1d').offset('2d').decay(0.5),
        ])
        .boostMode('multiply')
    )
    .from(from)
    .size(size)
    .toJSON()

  const res = await esSearch(requestBody)

  return {
    statusCode: 200,
    body: JSON.stringify({ data: res.hits }),
  }
}

export const handler = commonMiddleware(search)
