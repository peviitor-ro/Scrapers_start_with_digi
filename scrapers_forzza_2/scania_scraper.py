#
#
#
# Make a new scraper for PeViitor
# Link to this website ===> https://www.scania.com/ro/ro/home/about-scania/career/available-positions.html
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_global_headers() -> dict:
    """
    ... set global headers for new script. Scania scraping.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def get_data_from_scania(url: str) -> list:
    """
    Make a requests and return html with. Scrap data from html.
    """

    response = requests.get(url=url, headers=set_global_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='cmp-list__item list-children')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h4', class_='cmp-list__item-title').text
        link = sd.find('a', class_='cmp-list__item-link')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.scania.com' + link,
            "company": "scania",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def scrape_scania() -> None:
    """
    ...this is final function. It function store all data to json file.
    """

    final_data_scania = get_data_from_scania(
            'https://www.scania.com/ro/ro/home/about-scania/career/available-positions.html'
            )

    # save data to json file!
    with open('scrapers_forzza_2/data_scania.json', 'w') as new_file:
        json.dump(final_data_scania, new_file)

    print('Scania ---> Done!')
