#
#
#
#
# Company -> GMV
# Link ----> https://gmv.csod.com/ux/ats/careersite/4/home?c=gmv&lq=Russia&pl=ChIJ-yRniZpWPEURE_YRZvj9CRQ&country=ro&lang=en-US
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import re


# session for scraping
session = requests.Session()


def get_authorization_token() -> str:
    '''
    ... function for search Authorization key
    '''
    response = session.get(url='https://gmv.csod.com/ux/ats/careersite/4/home?c=gmv&lq=Russia&pl=ChIJ-yRniZpWPEURE_YRZvj9CRQ&country=ro&lang=en-US',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # find Authorization Token
    regex = r'"token":"([^"]+)"'
    matches = re.findall(regex, str(soup))
    if matches:
        token = matches[0]

    return token.strip()


def prepare_post_requests() -> tuple:
    '''
    ... here prepare post requests headers.
    '''

    auth_token = get_authorization_token()

    url = 'https://eu-fra.api.csod.com/rec-job-search/external/jobs'

    headers = {
        'authority': 'eu-fra.api.csod.com',
        'accept': 'application/json; q=1.0, text/*; q=0.8, */*; q=0.1',
        'accept-language': 'en-US,en;q=0.8',
        'authorization': f'Bearer {auth_token}',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'csod-accept-language': 'en-US',
        'origin': 'https://gmv.csod.com',
        'referer': 'https://gmv.csod.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    data = {
        "careerSiteId": 4,
        "careerSitePageId": 4,
        "pageNumber": 1,
        "pageSize": 25,
        "cultureId": 1,
        "searchText": "",
        "cultureName": "en-US",
        "states": [],
        "countryCodes": ["ro"],
        "cities": [],
        "placeID": "ChIJ-yRniZpWPEURE_YRZvj9CRQ",
        "radius": None,
        "postingsWithinDays": None,
        "customFieldCheckboxKeys": [],
        "customFieldDropdowns": [],
        "customFieldRadios": []
    }

    return url, headers, data


def collect_data_from_gmv() -> list[dict]:
    '''
    ...collect data with post reques.
    '''

    data = prepare_post_requests()

    response = session.post(url=data[0], headers=data[1], json=data[2]).json()

    lst_with_data = []
    for dt in response['data']['requisitions']:
        link = dt['requisitionId']
        title = dt['displayJobTitle']
        city = dt['locations'][0]['city']

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  f"https://gmv.csod.com/ux/ats/careersite/4/home/requisition/{link}?c=gmv&lang=en-US",
                    "company": "gmv",
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


company_name = 'gmv'
data_list = collect_data_from_gmv()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('gmv',
                  'data:image/png;base64,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'
                  ))
