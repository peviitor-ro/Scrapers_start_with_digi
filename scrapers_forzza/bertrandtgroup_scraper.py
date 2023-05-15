#
#
#
# Make new Scraper for bertrandtgroup --->
# Link to this Company ---> https://bertrandtgroup.onlyfy.jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import time
from random import randint


def set_headers():
    """
    Set special headers for requests to https://bertrandtgroup.onlyfy.jobs/.
    """

    headers = {
            'authority': 'bertrandtgroup.onlyfy.jobs',
            'accept': 'text/html, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.5',
            'referer': 'https://bertrandtgroup.onlyfy.jobs/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    return headers


# RETURN SOUP DATA
def get_soup_data(url: str):
    """
    Return Soup Data from site requests.
    """

    session = requests.Session()
    session.cookies = None

    response = session.get(url, headers=headers)

    print(response.content.decode())


def collect_data_from_site() -> list:
    """
    This func() return all data from site.
    """

    page = 1
    flag = None

    # collect data!
    lst_with_data = []
    while flag != 'no_data':

        soup = get_soup_data(url=f'https://bertrandtgroup.onlyfy.jobs/candidate/job/ajax_list?display_length=10&page={page}&sort=matching&sort_dir=DESC&_=1684168027359')

        # collect all data from sites
        soup_data_1 = soup.find_all('div', class_='row row-table row-24 collapsed row-table-condensed')
        soup_data_2 = soup.find_all('div', class_='row row-table row-24 collapsed even row-table-condensed')

        # all data in list!
        lst_with_data = []
        for sd in soup_data_1:
            link = sd.find('div', class_='inner').find('a')['href']
            title = sd.find('div', class_='inner').find('a').text

            # first data!
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://bertrandtgroup.onlyfy.jobs' + link,
                    "company": "bertrandtgroup",
                    "country": "Romania",
                    "city": "Romania"
                })

        for sd_2 in soup_data_2:
            link_2 = sd_2.find('div', class_='inner').find('a')['href']
            title_2 = sd_2.find('div', class_='inner').find('a').text

            # second data
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title_2,
                    "job_link":  'https://bertrandtgroup.onlyfy.jobs' + link_2,
                    "company": "bertrandtgroup",
                    "country": "Romania",
                    "city": "Romania"
                })

        next_page = soup.find('div', class_='row navigation pagination-next-container text-center')
        if next_page is not None:
            page += 1
        else:
            print('Scraper do all work!')
            flag = 'no_data'

    return lst_with_data


print(collect_data_from_site())
