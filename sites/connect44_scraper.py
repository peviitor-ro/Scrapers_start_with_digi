#
#
#
# Company -> connect44
# Link ----> https://www.connect44.com/careers/jobs?country=3&city=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


# session for new session!
session = requests.Session()


def csrf_and_session_tokens() -> str:
    '''
    '''

    response = requests.get(url='https://www.connect44.com/careers/jobs?country=3&search=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # token id and session id
    tokens = response.headers

    # catch csrf token
    meta_csrf = soup.find_all('meta')
    csrf = meta_csrf[-1]['content']

    return csrf, tokens


print(csrf_and_session_tokens())


def prepare_post_request() -> tuple:
    '''
    ... here, prepare url, headers and data for post request.
    '''

    url = 'https://www.connect44.com/livewire/message/jobs-table',

    headers = {
            'Accept': 'text/html, application/xhtml+xml',
          -H 'Accept-Language: en-US,en;q=0.5' \
          -H 'Connection: keep-alive' \
          -H 'Content-Type: application/json' \
          -H 'Cookie: CookieConsent={stamp:%27ND9DqhKFmppbOWaxrzR7/vmb82Rdt/kSiCvVQz3k06hyIo3E+8UlHA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1688208124784%2Cregion:%27ro%27}; XSRF-TOKEN=eyJpdiI6IllxekcxZHpCNHpUUEtROTY0Z3RVcUE9PSIsInZhbHVlIjoiSWxLcGgxZjVwYmd0Snc4TzFyekRjV1lYSHpaS2o4TzJ3NjBjeGExazYwOFNlQ0pUZVZaWTBtejZFTnZhdThlaGpsd1F3MlVkZU9ndnRvUzNMa2szcXBsQVFvd3I5dFRraW1QWkV6Sk1vdmtqNVdzQ2gzUWlReUlaU044RlZTVkYiLCJtYWMiOiJiYzliYjRlYTAxYWEwZTFhMjViOTU2NDFkMzM2ODA3YTA5OTQ1ZmE0MTc3MzQ5NGYyMTYyMWU1NjJhNTlmZDk1IiwidGFnIjoiIn0%3D; connect44_session=eyJpdiI6InR0ZUVYL1FTUGpmNFdZWVJ2dEwveXc9PSIsInZhbHVlIjoia0tWZ3dJNFRJRU1VNHhaUjgzL1N4eTNRTnhVazFtVlJDUUM2VFZUWDJMbHhDN0NMaW1QUmZ3R3JOb1lpSTFybnV5RUtsc1I0VE5qV2FkY2Yybmh6NnkyZHUrTGNJSFhXL2hraWlGblZCcXVKdVZvNTZpOVM3ZWQ2aitIOVl2eGIiLCJtYWMiOiJiY2RkMWE0ZDQ4OTdmZGFlZDgwZDBhNGUzNjUwNTdjNjdmMGI2Yjg3ZmM1NmUwZDZjMzZjZDAwYjQ2MjNhNzg4IiwidGFnIjoiIn0%3D' \
          -H 'Origin: https://www.connect44.com' \
          -H 'Referer: https://www.connect44.com/careers/jobs?country=3&city=' \
          -H 'Sec-Fetch-Dest: empty' \
          -H 'Sec-Fetch-Mode: cors' \
          -H 'Sec-Fetch-Site: same-origin' \
          -H 'Sec-GPC: 1' \
          -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
          -H 'X-CSRF-TOKEN: 3hIoEcyUENUf9j4cetdQavVmRU4wrZdPBdg2hzhF' \
          -H 'X-Livewire: true' \
  --data-raw '{"fingerprint":{"id":"I0zMkCYpbLINzhd23wYa","name":"jobs-table","locale":"en","path":"careers/jobs","method":"GET","v":"acj"},"serverMemo":{"children":[],"errors":[],"htmlHash":"16ff79d8","data":{"perPage":6,"search":null,"query":null,"country":"3","city":"","cities":[]},"dataMeta":{"modelCollections":{"cities":{"class":"App\\Models\\JobsCountryCity","id":[20,53],"relations":[],"connection":"tenant","collectionClass":null}}},"checksum":"ea7d114ce5e1d48ea71d61e4d02e257689cb46a37e96495192d62fe56b20266f"},"updates":[{"type":"callMethod","payload":{"id":"1zgk","method":"loadMore","params":[]}}]}' \
  --compressed
