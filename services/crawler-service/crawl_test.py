import requests
from requests.sessions import default_headers
from handlers.base_handler import requests_retry_session
from requests.adapters import HTTPAdapter
from requests.models import HTTPError
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def get_raw_html(url):
    text = ''
    try:
        response = requests.get(url, timeout=30)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        text = response.content
    finally:
        return text


url = 'https://www.thairath.co.th/home'
raw_html = get_raw_html(url).decode("utf-8")
soup = BeautifulSoup(raw_html, 'html.parser')

print(soup.find('div', id="section5"))

# with open('test.html', 'w') as f:
#     f.write(raw_html)
