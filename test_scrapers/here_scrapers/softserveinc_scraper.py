#
#
#
# New scraper for Company -> softserveinc
# link to jobs ---> https://career.softserveinc.com/en-us/vacancies/country-romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import time
from random import randint


def collect_data_from_site(page: int) -> list:
    """
    Collect all data from site.
    """

    response = requests.get(url=f'https://career.softserveinc.com/en-us/vacancy/search?country[]=romania&page={page}',
                            headers=DEFAULT_HEADERS)

    data_jobs = response.json()['data']

    lst_with_data = []
    for dj in data_jobs:
        link = dj['url']
        title = dj['name']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "softserveinc",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data


def run_scraper() -> tuple:
    """
    Scrap all data from softserveinc, and return big list.
    """

    page = 1
    flag = True

    big_lst_jobs = []
    while flag:

        # collect data from site!
        data_site = collect_data_from_site(page)

        if data_site:
            big_lst_jobs.extend(data_site)
            print(f'Scrape page {page}')

        else:
            print('Scraper do all job')
            flag = False

        page += 1

        #
        time.sleep(randint(1, 2))

    return big_lst_jobs, len(big_lst_jobs)
