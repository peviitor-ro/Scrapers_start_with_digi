#
#
#
#
# Company -> fisglobal
# Link ----> https://careers.fisglobal.com/us/en/search-results?s=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
import re
#
import json


def get_fresh_ids() -> tuple:
    '''
    ... get fresh data from site.
    '''

    res = requests.get(url='https://careers.fisglobal.com/us/en/search-results?s=1',
                       headers=DEFAULT_HEADERS)

    # get csrf Token
    csrf_token = re.search(r'"csrfToken":"(.*?)"', str(res.text)).group(1)

    # another ID from .headers!
    play_session = re.search(r'PLAY_SESSION=([^";]+)', str(res.headers)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^';]+)", str(res.headers)).group(0)

    return csrf_token, play_session, phpppe_act


def prepare_post_request() -> tuple:
    '''
    ... prepare post reques for collect data from json.
    '''

    # call data from function:
    data = get_fresh_ids()

    url = 'https://careers.fisglobal.com/widgets'

    headers = {
            'authority': 'careers.fisglobal.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'application/json',
            'cookie': f'VISITED_LANG=en; VISITED_COUNTRY=us; PHPPPE_GCC=a; PHPPPE_NPS=a; {data[1]}; {data[2]}',
            'origin': 'https://careers.fisglobal.com',
            'referer': 'https://careers.fisglobal.com/us/en/search-results?s=1',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-csrf-token': f'{data[0]}'
        }

    data = {
            "lang": "en_us",
            "deviceType": "desktop",
            "country": "us",
            "pageName": "search-results",
            "ddoKey": "eagerLoadRefineSearch",
            "sortBy": "",
            "subsearch": "",
            "from": 0,
            "jobs": True,
            "counts": True,
            "all_fields": ["category", "country", "state", "city", "jobType", "phLocSlider"],
            "size": 100,
            "clearAll": False,
            "jdsource": "facets",
            "isSliderEnable": True,
            "pageId": "page13",
            "siteType": "external",
            "keywords": "",
            "global": True,
            "selected_fields": {
                "country": ["Romania"]
            },
            "locationData": {
                "sliderRadius": 25,
                "aboveMaxRadius": True,
                "LocationUnit": "miles"
            },
            "s": "1"
        }

    return url, headers, data


def collect_data_from_fisglobal() -> list[dict]:
    '''
    ... get data after collecting all keys.
    '''

    n_data = prepare_post_request()

    response = requests.post(url=n_data[0], headers=n_data[1], data=json.dumps(n_data[2])).json()

    lst_with_data = []
    for job in response['eagerLoadRefineSearch']['data']['jobs']:
        title = job['title']
        link_final = f'https://careers.fisglobal.com/us/en/job/{job["jobId"]}/{job["applyUrl"].split("/")[-2].split("_")[0]}'
        city = job['city']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link_final,
                "company": "fisglobal",
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


company_name = 'fisglobal'
data_list = collect_data_from_fisglobal()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('fisglobal',
                  'https://cdn.phenompeople.com/CareerConnectResources/FIGLUS/images/SmallLogoBIv2-1668201955570.png'
                  ))
