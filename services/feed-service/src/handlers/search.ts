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
        .query(
          esb
            .boolQuery()
            .must(esb.multiMatchQuery().query(q).fields(['title', 'summary', 'tags']).operator('or'))
            .should(esb.matchPhraseQuery().field('title').query(q).boost(3))
            .should(esb.matchPhraseQuery().field('summary').query(q).boost(2))
            .should(esb.multiMatchQuery().query(q).fields(['title', 'summary']).operator('or').type('phrase').boost(4))
            .should(esb.multiMatchQuery().query(q).fields(['title', 'summary']).operator('and').boost(2))
            .should(esb.matchQuery('tags').query(q).boost(10))
        )
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
