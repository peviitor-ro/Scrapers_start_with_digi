#
#
#
# Scrap new company ---> thecoders
# link to jobs ---> https://adrya.ro/en/joburi/all/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_page(url: str) -> tuple:
    """
     Collect data ---> from the coders.
     --- in this code we have 1 flag. If flag is True,
     function continue collect data, if false, stopped.
     """

    response = requests.get(
            url=url,
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='inner')

    flag = True
    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a', class_='fancy red').text
        link = sd.find('a', class_='button bg-blue white iblock fs-12 mb-30 fancy')['data-href']

        # check if job is closed!
        closed_job = sd.find('li', class_='tags no-wrap pb-30').find('a', class_='red').text.strip()
        if closed_job == 'Closed':
            flag = False

            # stop collect data!
            continue

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "thecoders",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data, flag


def run_scraper() -> tuple:
    """
    Here, collect all data from site.
    Collect fresh data.
    """

    page = 1
    jobs_list_data = []

    while True:

        data = collect_data_from_page(
                url=f'https://adrya.ro/en/joburi/all/?page={page}')

        if len(data[0]) > 0:
            jobs_list_data.extend(data[0])
        elif data[1] == False:
            break

        page += 1

    return jobs_list_data, len(jobs_list_data)
