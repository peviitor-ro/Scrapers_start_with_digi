#
#
#
# Company Ubisoft
# Link -> https://www.ubisoft.com/en-us/company/careers/search?countries=ro!
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def prepare_post_request() -> tuple:
    """
    ... here prepare data for post requests.
    """

    url = 'https://avcvysejs1-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.8.4)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.11.0)%3B%20react%20(16.12.0)%3B%20react-instantsearch%20(6.8.3)&x-algolia-api-key=7d1048c332e18838e52ed9d41a50ac7b&x-algolia-application-id=AVCVYSEJS1'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ubisoft.com',
        'Referer': 'https://www.ubisoft.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
        }

    data_raw = {
            "requests": [
                {
                    "indexName": "jobs_en-us_default",
                    "params": "facetFilters=%5B%5B%22countryCode%3Aro%22%5D%5D&facets=%5B%22jobFamily%22%2C%22team%22%2C%22countryCode%22%2C%22cities%22%2C%22contractType%22%2C%22workFlexibility%22%2C%22graduateProgram%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&maxValuesPerFacet=100&page=0&query=&tagFilters="
                },
                {
                    "indexName": "jobs_en-us_default",
                    "params": "analytics=false&clickAnalytics=false&facets=countryCode&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=100&page=0&query="
                }
            ]
        }

    return url, headers, data_raw


def get_data_from_post_req() -> list:
    """
    ... make post request and collect data.
    """

    url, headers, data_raw = prepare_post_request()

    response = requests.post(url=url, headers=headers, json=data_raw).json()

    return response


print(get_data_from_post_req())
