const AWS = require('aws-sdk')

const personalizedEvent = new AWS.PersonalizeEvents({ apiVersion: '2018-03-22', region: 'ap-southeast-1' })

const event = {
  trackingId: '540f4295-c999-4252-ab41-a39882c83005',
  userId: '164591f3-2a53-4c94-84eb-da692dca55ca',
  sessionId: '00000000-00000000',
  eventList: [
    {
      sentAt: new Date(1613894208876),
      eventType: 'news_viewed',
      properties: { itemId: '26743cac-c411-4eb0-9e94-f689708cb948' },
    },
  ],
}

const res = personalizedEvent.putEvents(event, (err, data) => {
  if (err) console.log(err)
  console.log(data)
})
