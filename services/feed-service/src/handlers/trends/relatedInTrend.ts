import { Handler } from 'aws-lambda'
import commonMiddleware from '../../libs/commonMiddleware'
import { getTrends, searchNewsWithTrend, TrendWithTopics } from './common'

interface Event {
  queryStringParameters: {
    from: string
    size: string
    trend: string
  }
}

const relatedInTrend: Handler = async (event: Event, context) => {
  let { from = 0, size = 5, trend = '-1' } = event?.queryStringParameters
  from = Number(from)
  size = Number(size)

  const trends = await getTrends()
  const trendWithTopics = trends.find(({ trend: trendName }) => trendName === trend)

  if (trendWithTopics) {
    const res = await searchNewsWithTrend(trendWithTopics, { from, size })

    return {
      statusCode: 200,
      body: JSON.stringify({ data: res }),
    }
  } else {
    return { statusCode: 404 }
  }
}

export const handler = commonMiddleware(relatedInTrend)
