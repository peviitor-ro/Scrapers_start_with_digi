#
#
#
# New Scraper for peviitor.ro!
# link for this is ---> https://careers.egger.com/go/Jobs-in-Romania/8984955/
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_global_headers() -> dict:
    """
    Set global headers. Need for new requests.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def get_data_from_site() -> list:
    """
    This func() return all data from this site. Jobs scrap.
    """

    response = requests.get(
            url='https://careers.egger.com/go/Jobs-in-Romania/8984955/',
            headers=set_global_headers()
            )
    soup = BeautifulSoup(response.text, 'lxml')

    data_list = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for dl in data_list:
        link = dl.find('a')['href'].strip()
        title = dl.find('a').text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://careers.egger.com' + link,
            "company": "egger",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def egger_scraper():
    """
    Final func(). Store all data in JSON.
    """

    final_data = get_data_from_site()

    # save data to json
    with open('scrapers_forzza_2/data_egger.json', 'w') as new_file:
        json.dump(final_data, new_file)

    print('Egger ---> Done!')
