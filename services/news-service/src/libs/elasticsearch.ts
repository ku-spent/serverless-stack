import * as elasticsearch from 'elasticsearch'
import { ES_HOST } from '../constant'

export const elasticClient = new elasticsearch.Client({
  host: ES_HOST,
  log: 'error',
  connectionClass: require('http-aws-es'),
})
