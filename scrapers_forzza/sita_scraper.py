#
#
#
# New scraper for sita!
# Link for scrape is ---> https://globalhub-sita.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_headers():
    """
    Set default headers for scrap this site.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def collect_data_from_site(url: str) -> list:
    """
    This func() is about scraping data from sita job site.
    """

    response = requests.get(url=url, headers=set_headers())
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
            "company": "wirtek",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_sita_data


def sita_scrape():
    """
    This func() is base of all functions. Its logic of all code.
    """

    final_data = collect_data_from_site('https://globalhub-sita.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest')

    with open('scrapers_forzza/data_sita.json', 'w') as new_file:
        json.dump(final_data, new_file)

    print('Sita ---> Done!')
