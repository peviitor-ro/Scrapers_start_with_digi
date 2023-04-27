#
#
#
# Scrap this new site - Makita!
# Link to this site ---> https://makitajobs.ro/locuri-de-munca/
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_headers():
    """
    This func() is about setting headers for new requests.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def collect_data_from_makita(url: str) -> list:
    """
    Collect data from makita and return a list with dicts.
    """

    response = requests.get(url=url, headers=set_headers())
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

    return lst_with_data


def makita_scrape():
    """
    This func is about scrape makita website. Return all data in json.
    """

    final_data = collect_data_from_makita('https://makitajobs.ro/locuri-de-munca/')

    with open('scrapers_forzza/data_makita.json', 'w') as data_file:
        json.dump(final_data, data_file)

    print('Makita --> Done')
