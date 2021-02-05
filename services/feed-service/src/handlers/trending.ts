import { Handler } from 'aws-lambda'
import esb from 'elastic-builder'
import { esSearch } from '../libs/elasticsearch'
import commonMiddleware from '../libs/commonMiddleware'
import AWS from 'aws-sdk'
import { JsonWebTokenError } from 'jsonwebtoken'
import { TREND_LAMBDA_NAME } from '../constant'

const lambda = new AWS.Lambda()

interface TRENDING_RESPONSE {
  source: string
  trends: string[]
}

const search = async (trend: string) => {
  const requestBody = esb
    .requestBodySearch()
    .query(
      esb
        .functionScoreQuery()
        .query(
          esb
            .boolQuery()
            .must(esb.multiMatchQuery().query(trend).fields(['title', 'summary', 'tags']).operator('or'))
            .should(
              esb.multiMatchQuery().query(trend).fields(['title', 'summary']).operator('or').type('phrase').boost(4)
            )
            .should(esb.multiMatchQuery().query(trend).fields(['title', 'summary']).operator('and').boost(2))
            .should(esb.matchQuery('tags').query(trend).boost(10))
        )
        .functions([
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-7d').lt('now')).weight(5),
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-1m').lt('now-7d')).weight(2),
          esb.decayScoreFunction().field('pubDate').origin('now').scale('1d').offset('2d').decay(0.5),
        ])
        .boostMode('multiply')
    )
    .size(5)
    .toJSON()

  const res = await esSearch(requestBody)
  return { trend, news: res.hits.hits }
}

const trending: Handler = async (event, context) => {
  try {
    const { from = 0, size = 5 } = event?.queryStringParameters
    const data = await lambda
      .invoke({
        FunctionName: TREND_LAMBDA_NAME,
      })
      .promise()

    if (!data.Payload) throw Error("Doesn't recieve payload from invoke latest function")

    const response: TRENDING_RESPONSE = JSON.parse(data.Payload.toString())
    const { trends } = response
    const top_5_trend_with_news = await Promise.all(trends.slice(from, from + size).map((trend) => search(trend)))

    const body = { trends, feeds: top_5_trend_with_news }

    return {
      statusCode: 200,
      body: JSON.stringify(body),
    }
  } catch (error) {
    return {
      statusCode: 200,
      body: JSON.stringify(error),
    }
  }
}

export const handler = commonMiddleware(trending)
