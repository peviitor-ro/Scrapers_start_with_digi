#
#
#
# Scrape data from wirtek.com/compile
#
import requests
from bs4 import BeautifulSoup
#
import json


def set_headers():
    """
    This func() is about create headers for requests.
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def wirtek_scrape():
    """
    This func() is about scrape wirtek.
    """

    response = requests.get('https://www.wirtek.com/careers', headers=set_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    job_grid = soup.find_all('div', class_='careers-grid__job')
    
    for job in job_grid:
        



wirtek_scrape()
