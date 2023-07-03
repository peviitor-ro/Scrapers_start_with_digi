#
#
#
# Scrape new site - Procter & Gamble
# Link to this site ---> https://www.pgcareers.com/search-jobs?ascf=[{%27key%27:%27custom_fields.Language%27,%27value%27:%27English%27},]&alp=798549&alt=2
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import re
from math import ceil
import time


def get_csrf_token_and_ids() -> tuple:
    '''
    ... get new data from Procter&Gamble:
        - csrf token
        - web browser id
        - playsession.
    '''

    response = requests.get(url='https://www.pgcareers.com/global/en/search-results?from=0&s=1',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)

    # search for CSRF token
    csrf_token = soup.find('div', {'id': 'csrfToken'})

    return csrf_token


print(get_csrf_token_and_ids())
