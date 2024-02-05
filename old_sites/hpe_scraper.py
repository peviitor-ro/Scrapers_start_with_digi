#
#
#
# Company hpe
# Link -> https://careers.hpe.com/us/en/search-results
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import re


def get_cookie_and_csrf_token() -> tuple:
    """
    Get cookie and csrfToken from hpe website.
    """

    response_cookie = requests.get('https://careers.hpe.com/us/en/search-results',
                                   headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response_cookie.text, 'lxml')

    # -------> Search csfrToken
    regex = r'csrfToken":"([a-zA-Z0-9]+)"'
    match = re.search(regex, str(soup))
    if match:
        csrf_token = match.group(1)
    else:
        csrf_token = None

    # here return cookie
    cookie = response_cookie.headers['Set-Cookie']

    return cookie, csrf_token


def set_post_requests() -> tuple:
    """
    Here set post requests data for scraping HPE.
    """

    # here fresh cookie and csrfToken
    cookie, csrfToken = get_cookie_and_csrf_token()

    url = 'https://careers.hpe.com/widgets'

    headers = {
        'authority': 'careers.hpe.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        'content-type': 'application/json',
        'cookie': f'{cookie}',
        'origin': 'https://careers.hpe.com',
        'referer': 'https://careers.hpe.com/us/en/search-results',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-csrf-token': f'{csrfToken}'
        }

    params = {
            "lang": "en_us",
            "deviceType": "desktop",
            "country": "us",
            "pageName": "search-results",
            "ddoKey": "refineSearch",
            "sortBy": "",
            "subsearch": "",
            "from": 0,
            "jobs": True,
            "counts": True,
            "all_fields": ["category", "country", "state", "city", "type", "postalCode", "remote"],
            "size": 100,
            "clearAll": False,
            "jdsource": "facets",
            "isSliderEnable": False,
            "pageId": "page11",
            "siteType": "external",
            "keywords": "",
            "global": True,
            "selected_fields": {
                "country": ["Romania"]
            },
            "locationData": {}
        }

    return url, headers, params


def get_data_from_hpe() -> list:
    """
    ... collect all data from hpe website with fresh data.
    """

    url, headers, params = set_post_requests()

    response = requests.post(url=url, headers=headers, json=params).json()

    lst_with_data = []
    for dt in response['refineSearch']['data']['jobs']:
        title = dt['title']
        city = dt['cityState'].split()[0]

        #
        jobs_code = dt['jobSeqNo']

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  f"https://careers.hpe.com/us/en/job/{jobs_code}/{'-'.join(title.split())}",
                    "company": "hpe",
                    "country": "Romania",
                    "city": city
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'hpe'
data_list = get_data_from_hpe()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hpe',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Hewlett_Packard_Enterprise_logo.svg/530px-Hewlett_Packard_Enterprise_logo.svg.png?20210501045011'
                  ))
