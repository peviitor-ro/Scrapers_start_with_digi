#
#
#
# Scrape new Cpmpany -> Elektrobit
# link to this portal ---> https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]=
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_headers() -> dict:
    """
    Set global headers for new requests.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
        }

    return headers


def collect_data_from_website(url: str) -> list:
    """
    Collect data from elektrobit.
    """

    response = requests.get(url=url, headers=set_headers())
    soup = requests.get(response.text, 'lxml')

    soup_data = soup.find_all('tr', class_='alternative_1')

    lst_wiht = []
    for sd in soup_data:
        title = sd.find('a').text


        print(title)


collect_data_from_website(
        'https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]='
        )
