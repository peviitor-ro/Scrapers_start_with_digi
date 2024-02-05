#
#
#
#
# Company -> transperfect
# Link ----> https://transperfect.wd5.myworkdayjobs.com/transperfect?locations=04de9d10ef0101e811e2f443bc2ba9f3
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import re


# -------> !
session = requests.Session()


def get_ids() -> tuple:
    '''
    Get all needed ids for this site.
    '''

    response = session.head(url='https://transperfect.wd5.myworkdayjobs.com/transperfect?locations=04de9d10ef0101e811e2f443bc2ba9f3',
                           headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, ts_id, wday_vps, wd_browser_id


def prepare_post() -> tuple:
    '''
    Here prepare post request headers.
    '''

    play_session, csrf_token, ts_id, wday_vps, wd_browser_id = get_ids()

    url = 'https://transperfect.wd5.myworkdayjobs.com/wday/cxs/transperfect/transperfect/jobs'

    headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': f'{wday_vps} timezoneOffset=-180; {play_session} {ts_id} {wd_browser_id} {csrf_token[:-1]}',
            'Origin': 'https://transperfect.wd5.myworkdayjobs.com',
            'Referer': 'https://transperfect.wd5.myworkdayjobs.com/transperfect?locations=04de9d10ef0101e811e2f443bc2ba9f3',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-CALYPSO-CSRF-TOKEN': f'{csrf_token.split("=")[1]}'
            }

    data = {
        "appliedFacets": {
            "locations": ["04de9d10ef0101e811e2f443bc2ba9f3"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    return url, headers, data


def get_data_from_transperfect():
    '''
    ... get all data from site, after post requests with fresh cookie data.
    '''
    url, headers, data = prepare_post()

    response = session.post(url=url, headers=headers, json=data).json()

    lst_with_data = []
    for job in response['jobPostings']:
        title = job['title']
        link = 'https://transperfect.wd5.myworkdayjobs.com/en-US/transperfect' + job['externalPath']
        city = job['locationsText'].split('-')[1]

        lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "TransPerfect",
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


company_name = 'TransPerfect'
data_list = get_data_from_transperfect()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('TransPerfect',
                  'https://em-tti.eu/wp-content/uploads/2018/12/TP_Stacked_CMYK.jpg'
                  ))
