import { Handler } from 'aws-lambda'

import commonMiddleware from '../../libs/commonMiddleware'
import { TrendWithTopics, searchNewsWithTrend, getTrends } from './common'

const trending: Handler = async (event, context) => {
  try {
    const { from = 0, size = 5, newsSize = 3 } = event?.queryStringParameters
    const trends = await getTrends()
    const top_5_trend_with_news = await Promise.all(
      trends.map((trend) => searchNewsWithTrend(trend, { from: 0, size: newsSize }))
    )

    const withoutEmptyNews = top_5_trend_with_news.filter((trendingTopic) => trendingTopic.news.length > 0)

    const body = {
      trends: withoutEmptyNews.map(({ trend }) => trend),
      feeds: withoutEmptyNews.slice(from, from + size),
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ data: body }),
    }
  } catch (error) {
    return {
      statusCode: 200,
      body: JSON.stringify(error),
    }
  }
}

export const handler = commonMiddleware(trending)
