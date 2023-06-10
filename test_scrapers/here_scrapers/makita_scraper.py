#
#
#
# Scrap this new site - Makita!
# Link to this site ---> https://makitajobs.ro/locuri-de-munca/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def run_scraper(url='https://makitajobs.ro/locuri-de-munca/') -> tuple:
    """
    Collect data from makita and return a list with dicts.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='box-right')

    lst_with_data = []
    for data in soup_data:
        title = data.find('div', class_='content-title').text.strip()
        link = data.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://makitajobs.ro' + link,
            "company": "makita",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data, len(lst_with_data)
