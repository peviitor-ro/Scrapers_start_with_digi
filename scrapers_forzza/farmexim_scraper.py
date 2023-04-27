#
#
#
# New Scraper for Pirelli!
# Link for this job page ---> https://www.farmexim.ro/posturi-vacante-26.html
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_headers():
    """
    Set headers for farmexim. Go and Scrape this!
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def collect_data_from_farmexim(url: str) -> list:
    """
    Collect data from farmexim. All data from this site in one lst with dicts.
    """

    response = requests.get(url=url, headers=set_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='service-block-desc')

    lst_with_jobs = []
    for data in soup_data:
        link = data.find('a')['href']
        title = data.find('a').text.strip()

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.farmexim.ro' + link,
            "company": "farmexim",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_jobs


def farmexim_scrape():
    """
    Scrape data from farmexim site.
    """

    final_lst = collect_data_from_farmexim('https://www.farmexim.ro/posturi-vacante-26.html')

    with open('scrapers_forzza/data_farmexim.json', 'w') as data_file:
        json.dump(final_lst, data_file)

    print('Farmexim ---> Done!')
