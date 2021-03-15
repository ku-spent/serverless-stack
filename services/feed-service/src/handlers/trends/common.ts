import esb from 'elastic-builder'
import { TREND_LAMBDA_NAME } from '../../constant'
import { esSearch } from '../../libs/elasticsearch'
import AWS from 'aws-sdk'

export interface TrendWithTopics {
  trend: string
  topics: string[]
}

interface TRENDING_RESPONSE {
  source: string
  trends: TrendWithTopics[]
}

const lambda = new AWS.Lambda()

export const getTrends = async () => {
  const data = await lambda
    .invoke({
      FunctionName: TREND_LAMBDA_NAME,
    })
    .promise()

  if (!data.Payload) throw Error("Doesn't recieve payload from invoke latest function")

  const response: TRENDING_RESPONSE = JSON.parse(data.Payload.toString())

  return response.trends
}

export const searchNewsWithTrend = async (
  trendWithTopics: TrendWithTopics,
  { from = 0, size = 3 }: { from: number; size: number }
) => {
  const { trend, topics } = trendWithTopics
  const requestBody = esb
    .requestBodySearch()
    .query(
      esb
        .functionScoreQuery()
        .query(
          esb
            .boolQuery()
            .should(esb.termsQuery().values(topics).field('category'))
            .should(esb.termsQuery().values(topics).field('tags'))
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
    .minScore(100)
    .from(from)
    .size(size)
    .toJSON()

  const res = await esSearch(requestBody)
  return { trend, news: res.hits.hits }
}
