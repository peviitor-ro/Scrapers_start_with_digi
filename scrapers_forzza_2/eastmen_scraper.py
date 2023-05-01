#
#
#
# New Scraper for Eastemn.ro
# link to this site is ---> https://www.eastmen.ro/locuri-de-munca/
#
import requests
from bs4 import BeautifulSoup
#
import json
import uuid


def set_global_headers() -> dict:
    """
    ... this is a new headers for request to eastmen.ro
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
        }

    return headers


def get_request_eastmen(url: str) -> list:
    """
    ... this func() is about make a request to Eastmen and collect all data in a list.
    """

    response = requests.get(url=url, headers=set_global_headers())
    soup = BeautifulSoup(response.content, 'lxml')

    soup_data = soup.find_all('h2')

    lst_with_links = []
    for sd in soup_data:
        if sd.find('a'):
            link = sd.find('a')['href']
            title = sd.find('a').text

            lst_with_links.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "eastmen",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_links


def scrape_eastmen() -> None:
    """
    This func() is about save data in Json format for
    sending it to peviitor.ro.
    """

    data_final_list = get_request_eastmen('https://www.eastmen.ro/locuri-de-munca/')

    # save data to json!
    with open('scrapers_forzza_2/data_eastmen.json', 'w') as new_file:
        json.dump(data_final_list, new_file)

    print('Eastmen ---> Done!')
