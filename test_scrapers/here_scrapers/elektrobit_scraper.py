#
#
#
# Scrape new Cpmpany -> Elektrobit
# link to this portal ---> https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper(url='https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]=') -> tuple:
    """
    Collect data from elektrobit.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data_1 = soup.find_all('tr', class_='alternative_1')
    soup_data_2 = soup.find_all('tr', class_='alternative_0')

    lst_with_jobs = []

    # from tag 1
    for sd_1 in soup_data_1:
        title_1 = sd_1.find('a').text
        link_1 = sd_1.find('a')['href']

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title_1,
            "job_link":  link_1,
            "company": "elektrobit",
            "country": "Romania",
            "city": "Romania"
            })

    # from tag 2
    for sd_2 in soup_data_2:
        title_2 = sd_2.find('a').text
        link_2 = sd_2.find('a')['href']

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title_2,
            "job_link":  link_2,
            "company": "elektrobit",
            "country": "Romania",
            "city": "Romania"
            })

    # print num of all data
    print(f'Total nums of jobs from Elekrobit == {len(lst_with_jobs)}')

    return lst_with_jobs, len(lst_with_jobs)
