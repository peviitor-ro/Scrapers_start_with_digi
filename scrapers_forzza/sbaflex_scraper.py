#
#
#
# Company -> sbaflex!
# Link -> https://www.sbaflex.com/ro/locuri-de-munc%C4%83/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
from time import sleep
from random import randint


def set_post_param(page: int) -> tuple:
    '''
    ... set post param here. This site return data
    with post requests.
    '''

    url = 'https://www.sbaflex.com/ro/locuri-de-munc%C4%83/'

    headers = {
            'authority': 'www.sbaflex.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'application/json',
            'cookie': 'pll_language=ro',
            'origin': 'https://www.sbaflex.com',
            'referer': 'https://www.sbaflex.com/ro/locuri-de-munc%C4%83/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1'
        }

    param = {
            "action": "facetwp_refresh",
            "data": {
                "facets": {
                    "job_fields": [],
                    "city": [],
                    "job_title": [],
                    "total": [],
                    "load_more": []
                },
                "frozen_facets": {},
                "http_params": {
                    "get": [],
                    "uri": "ro/locuri-de-muncă",
                    "url_vars": [],
                    "lang": "ro"
                },
                "template": "wp",
                "extras": {
                    "selections": True,
                    "sort": "default"
                },
                "soft_refresh": 1,
                "is_bfcache": 1,
                "first_load": 0,
                "paged": f'{page}'
            }
        }

    return url, headers, param


def make_post_request(page: int) -> tuple:
    '''
    ... this func make post requests and return json() object.
    '''
    url, headers, param = set_post_param(page)

    response = requests.post(url=url,
                             headers=headers,
                             json=param)
    soup = BeautifulSoup(response.json()['template'], 'lxml')

    return response.json()['facets']['total'].split()[0], soup


def get_data_from_site() -> list:
    '''
    Start collect data. Jobsnum < 10,
    make one requests, else... Jobsnum / 10 iterations.
    '''
    num_jobs = int(make_post_request(1)[0]) + 2
    page = 1
    flag = True

    lst_with_data = []
    #
    while flag != False:

        data_post = make_post_request(page)

        if page <= (num_jobs // 10) + 2:

            # collect deta!
            for dt in data_post[1].find_all('div', class_='col-12 col-lg-10'):
                title = dt.find('h5', class_='title fs-4 mb-2 fw-bold').text.strip()
                link = dt.find('a', class_='btn btn-sm btn-orange mb-0 stretched-link text-nowrap')['href']
                city = dt.find('div', class_='badge bg-blue d-flex align-items-center').text.strip()

                if title:

                    lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "sbaflex",
                        "country": "Romania",
                        "city": city
                        })

            #
            print(f"Page {page} -> done!")

        else:
            flag = False

        page += 1

        # sleep!
        sleep(randint(1, 3))

    # return lst with data jobs
    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'sbaflex'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('sbaflex',
                  'https://www.sbaflex.com/wp-content/themes/employees/images/logo.svg'
                  ))
