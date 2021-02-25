import json
from difflib import SequenceMatcher
from helper import get_raw_html
from bs4 import BeautifulSoup

whitelist_topic = [
    'การศึกษา', 'การเมือง', 'กีฬา', 'คุณภาพชีวิต', 'ต่างประเทศ',
    'บันเทิง', 'ภาพยนตร์', 'สังคม', 'อาชญากรรม', 'เทคโนโลยี',
    'เศรษฐกิจ', 'ในประเทศ', 'ไลฟ์สไตล์'
]


def get_trends():
    source = 'thairath, google'

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    raw_html = get_raw_html('https://www.thairath.co.th/tags/trending')
    soup = BeautifulSoup(raw_html, 'html.parser')
    tags = soup.find('main').find('div').find_all('div', recursive=False)[2].find_all('div')[5].find_all('a')
    trends = [(tag.get_text(), tag['href']) for tag in tags]

    raw_html = get_raw_html('https://www.thairath.co.th/home').decode("utf-8")
    soup = BeautifulSoup(raw_html, 'html.parser')
    now_trends = [(elem.get_text(), elem['href']) for elem in soup.find('div', id="section5").find_all('a')]

    current_trends = now_trends + [trend for trend in trends if trend not in now_trends]

    # clean trends
    similar_trends = []
    similar_threshold = .8
    exclude_trends = ['วันนี้', 'รีไฟแนนซ์', 'ราคา', 'โปรแกรมฟุตบอล', 'ตารางคะแนน', 'ไทยรัฐ', 'thairath', 'ข่าว', 'ดวง', 'ตรวจหวย']
    current_trends = list(filter(lambda x: all([exclude not in x[0].lower() for exclude in exclude_trends]), current_trends))

    trends = [trend[0] for trend in current_trends]
    trends_url = ['https://www.thairath.co.th' + trend[1] for trend in current_trends]

    trends_with_topics = []
    for i in range(len(trends)):
        trend = trends[i]
        trend_url = trends_url[i]
        raw_html = get_raw_html(trend_url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        json_data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
        json_data = json_data['props']['initialState']['common']['data'].get('items')

        if(json_data is None):
            continue

        items = {}
        cur_depth = 0
        while not isinstance(items, list) and cur_depth < 5:
            key = list(json_data.keys())[0]
            items = json_data[key]
            json_data = items
            cur_depth += 1

        topics = [item['topic'] if item['topic'] in whitelist_topic else item['section'] for item in items]
        topics = [topic for topic in topics if topic in whitelist_topic]
        topics = list(set(topics))
        if(len(topics) > 0):
            trends_with_topics.append({'trend': trend, 'topics': topics})

    raw_html = get_raw_html('https://trends.google.co.th/trends/trendingsearches/daily/rss?geo=TH')
    soup = BeautifulSoup(raw_html, 'xml')

    items = soup.findAll('item')
    google_trends = [{'trend': item.find('title').string, 'topics': item.find('description').get_text().split(', ')} for item in soup.findAll('item')]

    all_trends = google_trends + trends_with_topics

    # find similar trends
    for i in range(len(all_trends)):
        for j in range(i + 1, len(all_trends)):
            trend_1 = all_trends[i]['trend']
            trend_2 = all_trends[j]['trend']

            sim_val = similar(trend_1, trend_2)
            if(sim_val > similar_threshold):
                similar_trends.append((trend_1, trend_2))
            elif(trend_1 in trend_2):
                similar_trends.append((trend_1, trend_2))
            elif(trend_2 in trend_1):
                similar_trends.append((trend_1, trend_2))
    for similar_trend in similar_trends:
        # remove larger trend length
        trend_1 = similar_trend[0]
        trend_2 = similar_trend[1]
        to_remove_trend = trend_1 if len(trend_1) > len(trend_2) else trend_2
        # remove one similar trend
        for index, item in enumerate(all_trends):
            if(item['trend'] == to_remove_trend):
                del all_trends[index]
                break

    return all_trends, source
