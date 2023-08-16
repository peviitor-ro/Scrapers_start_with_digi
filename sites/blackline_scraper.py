#
#
#
#
# Company -> blackline
# Link ----> https://careers.blackline.com/careers-home/jobs?page=2&location=Romania&woe=12&stretchUnit=MILES&stretch=10
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import re
from time import sleep


# start session
session = requests.Session()


def get_secret_data():
    '''
    Get secret data from blackline.
    '''

    res_secret = session.get(url='https://careers.blackline.com/careers-home/jobs?page=1&location=Romania&woe=12&stretchUnit=MILES&stretch=10',
                              headers=DEFAULT_HEADERS).headers

    # search data with regex!
    jassesion = re.search(r"jasession=([^;]+)", str(res_secret)).group(1)
    jrassision = re.search(r"jrasession=([a-fA-F0-9-]+)", str(res_secret)).group(1)

    return jassesion, jrassision


def prepare_post_requests(page: str) -> tuple:
    '''
    Here prepare post requests with secret data.
    '''

    data_requests = get_secret_data()

    url = f'https://careers.blackline.com/api/jobs?page={page}&location=Romania&woe=12&stretchUnit=MILES&stretch=10&sortBy=relevance&descending=false&internal=false'
    headers = {
            'authority': 'careers.blackline.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.6',
            'cookie': f'i18n=en-US; searchSource=external; {data_requests[1]}; {data_requests[0]}; pixel_consent=%7B%22cookie%22%3A%22pixel_consent%22%2C%22type%22%3A%22cookie_notice%22%2C%22value%22%3Atrue%2C%22timestamp%22%3A%222023-07-12T17%3A20%3A07.446Z%22%7D',
            'referer': f'https://careers.blackline.com/careers-home/jobs?page={page}&location=Romania&woe=12&stretchUnit=MILES&stretch=10',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    return url, headers


def collect_data_from_blackline() -> list[dict]:
    '''
    ... collect data from blackline:
        -> make a request to API.
        ... only requests library.
    '''

    page_req = 1
    lst_with_data = []

    flag = True
    while flag != False:

        post_request = prepare_post_requests(page_req)
        response = session.get(url=post_request[0], headers=post_request[1]).json()['jobs']
        #
        if len(response) > 1:
            for job in response:
                link_id = job['data']['slug']
                title = job['data']['title']
                city = job['data']['location_name']
                print(city)

                if 'bucharest' in city.lower():

                    lst_with_data.append({
                            "id": str(uuid.uuid4()),
                            "job_title": title,
                            "job_link":  f'https://careers.blackline.com/careers-home/jobs/{link_id}?lang=en-us',
                            "company": "BlackLine",
                            "country": "Romania",
                            "city": city
                        })

        else:
            flag = False

        page_req += 1

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BlackLine'
data_list = collect_data_from_blackline()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('BlackLine',
                  'https://cms.jibecdn.com/prod/blackline/assets/HEADER-NAV_LOGO-en-us-1640926577769.svg'))
