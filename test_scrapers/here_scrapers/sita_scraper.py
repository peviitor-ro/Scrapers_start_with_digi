#
#
#
# New scraper for sita!
# Link for scrape is ---> https://globalhub-sita.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def run_scraper(url='https://globalhub-sita.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest') -> tuple:
    """
    This func() is about scraping data from sita job site.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    all_data = soup.find_all('div', class_='col-xs-12 title')

    lst_with_sita_data = []
    for data in all_data:
        link_job = data.find('a')['href']
        title_job = data.find('h2').text.strip()

        lst_with_sita_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title_job,
            "job_link":  link_job,
            "company": "sita",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_sita_data, len(lst_with_sita_data)
