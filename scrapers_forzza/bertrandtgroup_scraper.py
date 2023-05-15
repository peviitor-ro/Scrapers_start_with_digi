#
#
#
# Make new Scraper for bertrandtgroup --->
# Link to this Company ---> https://bertrandtgroup.onlyfy.jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import time
from random import randint


def set_headers():
    """
    Set special headers for requests to https://bertrandtgroup.onlyfy.jobs/.
    """

    headers = {
            'authority': 'bertrandtgroup.onlyfy.jobs',
            'accept': 'text/html, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.5',
            'referer': 'https://bertrandtgroup.onlyfy.jobs/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    return headers


# RETURN SOUP DATA
def get_soup_data(url: str):
    """
    Return Soup Data from site requests.
    """

    session = requests.Session()
    session.cookies = None

    response = session.get(url, headers=headers)

    print(response.content.decode())

    
print(get_soup_data()
