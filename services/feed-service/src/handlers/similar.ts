import { Handler } from 'aws-lambda'
import esb from 'elastic-builder'
import { ES_INDEX } from '../constant'
import commonMiddleware from '../libs/commonMiddleware'
import { esSearch } from '../libs/elasticsearch'

const getDocById = async (id: string) => {
  const requestBody = esb.requestBodySearch().query(esb.matchQuery().field('id').query(id)).size(1).toJSON()
  const res = await esSearch(requestBody)
  return res.hits.hits.length > 0 ? res.hits.hits[0] : null
}

const similar: Handler = async (event, context) => {
  const { from = 0, size = 5, id } = event?.queryStringParameters

  const doc = await getDocById(id)

  if (!doc)
    return {
      statusCode: 404,
    }

  const searchDoc = { _index: ES_INDEX, _id: doc._id }
  const body = esb
    .requestBodySearch()
    .query(
      esb
        .functionScoreQuery()
        .query(
          esb
            .boolQuery()
            .should([
              esb.moreLikeThisQuery().fields(['title', 'sumamry']).like(searchDoc).boost(4),
              esb.moreLikeThisQuery().fields(['category']).like(searchDoc).minTermFreq(1).maxQueryTerms(12).boost(2),
            ])
            .should((doc['_source'] as any)['tags'].map((tag: string) => esb.termQuery('tags', tag).boost(4)))
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

export const handler = commonMiddleware(similar)
