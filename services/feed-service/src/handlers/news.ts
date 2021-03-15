import { Handler } from 'aws-lambda'
import esb, { boolQuery, matchAllQuery, matchQuery, termQuery, termsQuery } from 'elastic-builder'
import commonMiddleware from '../libs/commonMiddleware'
import { esSearch } from '../libs/elasticsearch'

const news: Handler = async (event, context) => {
  const {
    from = 0,
    size = 5,
    query,
    queryField = '_',
    filterCategories,
    filterSources,
    filterTags,
  } = event?.queryStringParameters

  // const filterTags: string[] = []
  // const filterSources: string[] = ['มติชน']
  // const filterCategories: string[] = ['การเมือง']

  let filterQuery = boolQuery().must(query ? matchQuery(queryField, query) : matchAllQuery())
  const filterObj = {
    category: filterCategories,
    source: filterSources,
    tags: filterTags,
  }

  try {
    Object.keys(filterObj).map((field) => {
      if (filterObj[field]) {
        const parsedValues: string[] = JSON.parse(filterObj[field])
        if (!(parsedValues instanceof Array)) return { statusCode: 400 }
        filterQuery = filterQuery.mustNot(termsQuery().field(field).values(parsedValues))
      }
    })
  } catch {
    return { statusCode: 400 }
  }

  const body = esb
    .requestBodySearch()
    .query(filterQuery)
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
