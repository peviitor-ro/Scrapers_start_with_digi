#
#
#
# New scraper for peviitor.ro!
# Link to this jobs ---> https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_global_headers() -> dict:
    """
    Set global headers for this new site -> Jumbo!
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
        }

    return headers


def get_data_from_jumbo(url: str) -> list:
    """
    This func() return data from jumbo page.
    """

    response = requests.get(url=url, headers=set_global_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('article', class_='x-control x-box x-article-box careers-article')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='title').text
        link = sd.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://corporate.e-jumbo.gr' + link,
            "company": "jumbo",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def scrapep_jumbo() -> None:
    """
    ... this func() is about scraping data.
    """

    final_list_jobs = get_data_from_jumbo(
            'https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/'
            )

    with open('scrapers_forzza_2/data_jumbo.json', 'w') as new_file:
        json.dump(final_list_jobs, new_file)

    print('Jumbo ---> Done')
