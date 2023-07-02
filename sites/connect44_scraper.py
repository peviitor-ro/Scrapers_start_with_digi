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
import re


# session for new session!
session = requests.Session()


def csrf_and_session_tokens() -> tuple[str]:
    '''
    '''

    response = session.get(url='https://www.connect44.com/careers/jobs?country=3&search=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # token id and session id
    tokens = response.headers
    x_csrf = re.search(r'XSRF-TOKEN=([^;]+)', str(tokens)).group(0)
    connec44_id = re.search(r'connect44_session=([^;]+)', str(tokens)).group(0)

    # check sum
    div_elements = soup.find_all('div', attrs={'wire:id': True})
    wire_ids = [div['wire:id'] for div in div_elements]

    # htmlHash
    html_hash_regex = r'htmlHash":"([^"]+)'
    html_hash_match = re.search(html_hash_regex, str(div_elements))
    if html_hash_match:
        html_hash = html_hash_match.group(1)

    # v Value!
    v_regex = r'"v":"([^"]+)'
    v_match = re.search(v_regex, str(div_elements))
    if v_match:
        v_value = v_match.group(1)

    # search for checksum
    regex = r'checksum":"([^"]+)"'
    matches = re.findall(regex, str(div_elements))
    if matches:
        checksum = matches[0]

    # catch csrf token
    meta_csrf = soup.find_all('meta')
    csrf = meta_csrf[-1]['content']

    return csrf, x_csrf, connec44_id, wire_ids[0], checksum, html_hash, v_value


def prepare_post_request() -> tuple:
    '''
    ... here, prepare url, headers and data for post request.
    '''

    data = csrf_and_session_tokens()

    url = 'https://www.connect44.com/livewire/message/jobs-table',

    headers = {

            'Accept': 'text/html, application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': f'CookieConsent={"stamp:%27ND9DqhKFmppbOWaxrzR7/vmb82Rdt/kSiCvVQz3k06hyIo3E+8UlHA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1688208124784%2Cregion:%27ro%27"}; {data[1]}; {data[2]};',
            'Origin': 'https://www.connect44.com',
            'Referer': 'https://www.connect44.com/careers/jobs?country=3&city=',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-CSRF-TOKEN': f'{data[0]}',
            'X-Livewire': 'true'
            }

    json_data = {
            'fingerprint': {
                'id': f'{data[3]}',
                'name': 'jobs-table',
                'locale': 'en',
                'path': 'careers/jobs',
                'method': 'GET',
                'v': f'{data[6]}'
            },
            'serverMemo': {
                'children': [],
                'errors': [],
                'htmlHash': f'{data[5]}',
                'data': {
                    'perPage': 6,
                    'search': None,
                    'query': None,
                    'country': '3',
                    'city': '',
                    'cities': []
                },
                'dataMeta': {
                    'modelCollections': {
                        'cities': {
                            'class': 'App\\Models\\JobsCountryCity',
                            'id': [20, 53],
                            'relations': [],
                            'connection': 'tenant',
                            'collectionClass': None
                        }
                    }
                },
                'checksum': f'{data[5]}'
            },
            'updates': [
                {
                    'type': 'callMethod',
                    'payload': {
                        'id': '1zgk',
                        'method': 'loadMore',
                        'params': []
                    }
                }
            ]
        }

    return url, headers, json_data


def collect_data_from_connect44() -> list[dict]:
    '''
    ... collect data with prepared headers.
    '''

    post_data = prepare_post_request()

    response = session.post(url=post_data[0], headers=post_data[1], json=post_data[2])
    print(response)


print(collect_data_from_connect44())
