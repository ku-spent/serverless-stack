import { Handler } from 'aws-lambda'
import esb from 'elastic-builder'
import { ES_INDEX } from '../constant'
import commonMiddleware from '../libs/commonMiddleware'
import { esSearch } from '../libs/elasticsearch'

const related: Handler = async (event, context) => {
  const { from = 0, size = 5, _id } = event?.queryStringParameters

  const searchDoc = { _index: ES_INDEX, _id }

  const body = esb
    .requestBodySearch()
    .query(
      esb
        .functionScoreQuery()
        .query(
          esb
            .boolQuery()
            .should([
              esb
                .moreLikeThisQuery()
                .fields(['title', 'sumamry', 'tag'])
                .like(searchDoc)
                .minTermFreq(1)
                .maxQueryTerms(12)
                .boost(2),
              esb.moreLikeThisQuery().fields(['category']).like(searchDoc).minTermFreq(1).maxQueryTerms(12).boost(10),
            ])
        )
        .functions([
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-7d').lt('now')).weight(5),
          esb.weightScoreFunction().filter(esb.rangeQuery('pubDate').gte('now-1m').lt('now-7d')).weight(2),
          esb.decayScoreFunction().field('pubDate').origin('now').scale('1d').offset('2d').decay(0.5),
        ])
        .boostMode('sum')
    )
    .from(from)
    .size(size)
    .toJSON()

  const res = await esSearch(body)

  return {
    statusCode: 200,
    body: JSON.stringify({ data: res.hits }),
  }
}

export const handler = commonMiddleware(related)
