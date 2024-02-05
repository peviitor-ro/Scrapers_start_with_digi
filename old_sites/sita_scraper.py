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


def collect_data_from_site(url: str) -> list:
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

    return lst_with_sita_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'sita'
data_list= collect_data_from_site('https://globalhub-sita.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest')
scrape_and_update_peviitor(company_name, data_list)
