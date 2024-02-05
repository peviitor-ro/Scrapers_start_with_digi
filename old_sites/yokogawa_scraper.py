#
#
#
#
# Company -> yokogawa
# Link ----> https://www.yokogawa.com/about/careers/careers-at-yokogawa/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
import re


def get_unic_ids() -> tuple:
    '''
    ... get unic ids from site.
    '''

    response = requests.head(url='https://wd3.myworkdaysite.com/recruiting/yokogawa/yokogawa-career-site',
                             headers=DEFAULT_HEADERS)
    data_res = str(response.headers)

    # collect needed data!
    play_session = re.findall(r'PLAY_SESSION=.*?(?:[;&]|$)', data_res)[0]
    wday_vps = re.search(r'wday_vps_cookie=(.*?)(?:[;]|$)', data_res).group(0)
    ts_TS = re.search(r'TS01292a30=(.*?)(?:[;]|$)', data_res).group(0)
    wd_browser_id = re.search(r'wd-browser-id=(.*?)(?:[;]|$)', data_res).group(0)
    calypso_csrf_token = re.search(r'CALYPSO_CSRF_TOKEN=(.*?)(?:[;]|$)', data_res).group(0)

    return play_session, wday_vps, ts_TS, wd_browser_id, calypso_csrf_token


def prepare_post_headers() -> tuple:
    '''
    Prepare post requests with headers from site.
    '''

    play_session, wday_vps, ts_TS, wd_browser_id, calypso_csrf_token = get_unic_ids()

    url = 'https://wd3.myworkdaysite.com/wday/cxs/yokogawa/yokogawa-career-site/jobs'

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': f'{play_session}; {wday_vps} {ts_TS} timezoneOffset=-180; {wd_browser_id} {calypso_csrf_token[:-1]}',
        'Origin': 'https://wd3.myworkdaysite.com',
        'Referer': 'https://wd3.myworkdaysite.com/recruiting/yokogawa/yokogawa-career-site',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': f'{calypso_csrf_token.split("=")[1]}'
        }

    data = {
        "appliedFacets": {
            "locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]
        },
        "searchText": ""
        }

    return url, headers, data


def collect_data_from_yokogawa():
    '''
    ... return data from site, after post request.
    '''

    url, headers, data = prepare_post_headers()

    response = requests.post(url=url, headers=headers, json=data).json()

    lst_with_data = []
    for job in response['jobPostings']:
        title = job['title']
        link = job['externalPath']
        #location = job['locationsText']

        lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link": f'https://wd3.myworkdaysite.com/en-US/recruiting/yokogawa/yokogawa-career-site{link}?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
                        "company": "yokogawa",
                        "country": "Romania",
                        "city": "Bucuresti",
                        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'yokogawa'
data_list = collect_data_from_yokogawa()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('yokogawa',
                  'https://web-material3.yokogawa.com/1/10029/tabs/trademark.jpg'
                  ))
