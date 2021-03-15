import { APIGatewayEvent, Handler } from 'aws-lambda'
import esb, { boolQuery, matchAllQuery, matchQuery, termQuery, termsQuery } from 'elastic-builder'
import commonMiddleware from '../libs/commonMiddleware'
import { esSearch } from '../libs/elasticsearch'

interface Event extends APIGatewayEvent {
  queryStringParameters: {
    from: string
    size: string
    query: string
    queryField: string
  }
  multiValueQueryStringParameters: {
    filterCategories: string[]
    filterSources: string[]
    filterTags: string[]
  }
}

const news: Handler = async (event: Event, context) => {
  const { from = 0, size = 5, query, queryField = '_' } = event.queryStringParameters

  const { filterCategories, filterSources, filterTags } = event.multiValueQueryStringParameters

  let filterQuery = boolQuery().must(query ? matchQuery(queryField, query) : matchAllQuery())
  const filterObj = {
    category: filterCategories,
    source: filterSources,
    tags: filterTags,
  }

  Object.keys(filterObj).map((field) => {
    if (filterObj[field]) {
      filterQuery = filterQuery.mustNot(termsQuery().field(field).values(filterObj[field]))
    }
  })

  const body = esb
    .requestBodySearch()
    .query(filterQuery)
    .sort(esb.sort('pubDate', 'desc'))
    .from(+from)
    .size(+size)
    .toJSON()

  const res = await esSearch(body)

  console.log(res.hits)

  return {
    statusCode: 200,
    body: JSON.stringify({ data: res.hits }),
  }
}

export const handler = commonMiddleware(news)
