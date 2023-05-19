#
#
#
# Make new Scraper for bertrandtgroup --->
# Link to this Company ---> https://bertrandtgroup.onlyfy.jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import time
from random import randint


def return_soup(url: str):
    """
    ... return soup object from link.
    """
    response = requests.get(
            url=


def get_soup_data(url: str) -> int:
    """
    Return total nums of jobs from Bertrandtgroup
    """
    


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
