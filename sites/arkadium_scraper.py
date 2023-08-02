#
#
#
#
# Company -> arkadium
# Link ----> https://corporate.arkadium.com/careers/we-are-hiring/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


session = requests.Session()


def get_cookie() -> tuple:
    '''
    ... get all cookies from site. Need for post requests fresh headers.
    '''

    response = session.head(url='https://apply.workable.com/arkadium-1/',
                             headers=DEFAULT_HEADERS).headers['set-cookie'].split(';')

    id_1 = response[0].strip()
    id_2 = response[5].split(',')[-1].strip()

    return id_1, id_2


def prepare_post_request() -> tuple:
    '''
    ... here prepare post requests.
    '''

    first_id, second_id = get_cookie()

    url = 'https://apply.workable.com/api/v3/accounts/arkadium-1/jobs'

    headers = {
        'authority': 'apply.workable.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'content-type': 'application/json',
        'cookie': f'{first_id}; {second_id}; _dd_s=rum=0&expire=1691004117342',
        'origin': 'https://apply.workable.com',
        'referer': 'https://apply.workable.com/arkadium-1/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    payload = {
        "query": "",
        "location": [],
        "department": [],
        "worktype": [],
        "remote": []
        }

    return url, headers, payload


def collect_data_from_arkadium() -> list[dict]:
    '''
    ... return all data after post requests.
    '''

    url, headers, payload = prepare_post_request()

    res = session.post(url=url, headers=headers, json=payload).json()

    lst_with_data = []
    for job in res['results']:
        title = job['title']
        link = f"https://apply.workable.com/arkadium-1/j/{job['shortcode']}/"
        location = job['location']['country']

        if location == 'Romania':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "arkadium",
                "country": "Romania",
                "city": location
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'arkadium'
data_list = collect_data_from_arkadium()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('arkadium',
                  'https://workablehr.s3.amazonaws.com/uploads/account/logo/233867/Logo_small.png'
                  ))
