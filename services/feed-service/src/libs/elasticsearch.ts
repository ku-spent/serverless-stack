import * as elasticsearch from 'elasticsearch'

export const elasticClient = new elasticsearch.Client({
  host: process.env.ES_HOST,
  log: 'error',
  connectionClass: require('http-aws-es'),
})

export const esSearch = async (body: any) =>
  elasticClient.search({
    index: process.env.ES_INDEX_RSS,
    body,
  })
