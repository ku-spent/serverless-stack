import middy from '@middy/core'
import httpJsonBodyParser from '@middy/http-json-body-parser'
import httpEventNormalizer from '@middy/http-event-normalizer'
import httpErrorHandler from '@middy/http-error-handler'
import { Handler } from 'aws-lambda'

const commonMiddleware = (handler: Handler) =>
  middy(handler).use(httpJsonBodyParser()).use(httpEventNormalizer()).use(httpErrorHandler())

export default commonMiddleware
