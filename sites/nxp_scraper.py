#
#
#
# Company -> nxp
# Link -> https://nxp.wd3.myworkdayjobs.com/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import re
from math import ceil
from time import sleep


# make a session for this site!
s = requests.Session()


def get_session_id_ts():
    '''
    ... return sessin id TS and more over.
    '''

    response = requests.get(url='https://nxp.wd3.myworkdayjobs.com/careers?locations=f2e609fe92974a55a05fc1cdc2852122',
                             headers=DEFAULT_HEADERS)

    return response.headers['Set-Cookie']


def prepare_headers_post_requests() -> tuple:
    '''
    ... here prepare post requests for scraping data.
    '''

    # get fresh headers every time script make a new posts requests.
    fresh_headers = get_session_id_ts()

    wday_vps_cookie = re.search(r"wday_vps_cookie=(\d+\.\d+\.\d+)", fresh_headers).group(0)
    play_session = re.search(r"PLAY_SESSION=([a-zA-Z0-9\-]+)-nxp_pSessionId=([a-zA-Z0-9]+)&instance=([a-zA-Z0-9]+);",
                             fresh_headers).group(0)
    ts_id = re.search(r"TS014c1515=([a-fA-F0-9]+);", fresh_headers).group(0)
    web_browser_id = re.search(r"wd-browser-id=([a-fA-F0-9\-]+);", fresh_headers).group(0)
    calypso = re.search(r"CALYPSO_CSRF_TOKEN=([a-fA-F0-9\-]+)", fresh_headers).group(0)
    calypso_split = calypso.split('=')[-1]

    url = 'https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs'

    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': f"{wday_vps_cookie};  timezoneOffset=-180; {play_session} {ts_id} {web_browser_id} {calypso}",
            'Origin': 'https://nxp.wd3.myworkdayjobs.com',
            'Referer': 'https://nxp.wd3.myworkdayjobs.com/careers?Location_Country=f2e609fe92974a55a05fc1cdc2852122',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-CALYPSO-CSRF-TOKEN': f"{calypso_split}",
        }

    return url, headers


def collect_data_from_nxp() -> list[dict]:
    '''
    ... collect data from nxp. Need all data.
    '''

    # here catch a number of jobs.
    data = prepare_headers_post_requests()
    jobs_num = s.post(url=data[0], headers=data[1],
                      json={
                          "appliedFacets": {"Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
                          "limit": 20,
                          "offset": 0,
                          "searchText": ""
                          }).json()['total']

    for_loop_offset = 0
    lst_with_data = []
    for _ in range(ceil(jobs_num / 20)):

        # make a post requests
        jobs_post_data = s.post(url=data[0], headers=data[1],
                                json={
                                      "appliedFacets": {"Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
                                      "limit": 20,
                                      "offset": f"{for_loop_offset}",
                                      "searchText": ""
                                      }).json()

        # collect data from json
        for i_jobs in jobs_post_data['jobPostings']:
            title = i_jobs['title']
            link = i_jobs['externalPath']
            location = i_jobs['locationsText']

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": 'https://nxp.wd3.myworkdayjobs.com/en-US/careers' + link,
                    "company": "nxp",
                    "country": "Romania",
                    "city": location
                })

        # increment for_loop_offset
        for_loop_offset += 20
        sleep(1)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'nxp'
data_list = collect_data_from_nxp()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('nxp',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/NXP-Logo.svg/618px-NXP-Logo.svg.png?20150315023951'
                  ))
