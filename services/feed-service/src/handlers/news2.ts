import AWS from 'aws-sdk'
import { APIGatewayEvent, Handler } from 'aws-lambda'
import { boolQuery, matchAllQuery, matchQuery, termQuery, termsQuery } from 'elastic-builder'
import commonMiddleware from '../libs/commonMiddleware'
import { QueryInput } from 'aws-sdk/clients/dynamodb'

interface Event extends APIGatewayEvent {
  queryStringParameters: {
    from: string
    size: string
    query: string
    queryField: string
    lastEvaluatedKey: string
  }
  multiValueQueryStringParameters: {
    filterCategories: string[]
    filterSources: string[]
    filterTags: string[]
  }
}

const dynamodb = new AWS.DynamoDB({ apiVersion: '2012-08-10' })

const news: Handler = async (event: Event, context) => {
  const { from = '0', size = '5', query = 'news', queryField = 'type', lastEvaluatedKey } = event.queryStringParameters

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

  const exclusiveStartKey = lastEvaluatedKey ? JSON.parse(lastEvaluatedKey) : undefined

  let indexName = ''

  switch (queryField) {
    case 'source':
      indexName = 'LatestNewsOnSources'
      break
    case 'category':
      indexName = 'LatestNewsOnCategory'
      break
    default:
      indexName = 'LatestNews'
      break
  }

  console.log(queryField, query, indexName)

  const params: QueryInput = {
    TableName: 'News2',
    IndexName: indexName,
    KeyConditionExpression: `#${queryField} = :val`,
    ExpressionAttributeNames: {
      [`#${queryField}`]: queryField,
    },
    ExpressionAttributeValues: {
      ':val': {
        S: query,
      },
    },
    Limit: Number(size),
    ExclusiveStartKey: exclusiveStartKey,
    ScanIndexForward: false,
  }
  console.log(params)
  const res = await dynamodb.query(params).promise()
  const items = res.Items ? res.Items.map((item) => AWS.DynamoDB.Converter.unmarshall(item)) : null
  return {
    statusCode: 200,
    body: JSON.stringify({
      data: { hits: items, lastEvaluatedKey: res.LastEvaluatedKey ? JSON.stringify(res.LastEvaluatedKey) : undefined },
    }),
  }
}

export const handler = commonMiddleware(news)
