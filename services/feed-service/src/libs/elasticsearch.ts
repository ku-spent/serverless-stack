import * as elasticsearch from 'elasticsearch'
import { ES_HOST, ES_INDEX } from '../constant'

export const elasticClient = new elasticsearch.Client({
  host: ES_HOST,
  log: 'error',
  connectionClass: require('http-aws-es'),
})

export const esSearch = async (body: any) =>
  elasticClient.search({
    index: ES_INDEX,
    body,
  })
