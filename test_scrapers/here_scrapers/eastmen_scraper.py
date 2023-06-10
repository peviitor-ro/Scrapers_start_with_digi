#
#
#
# New Scraper for Eastemn.ro
# link to this site is ---> https://www.eastmen.ro/locuri-de-munca/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper(url='https://www.eastmen.ro/locuri-de-munca/') -> tuple:
    """
    ... this func() is about make a request to Eastmen and collect all data in a list.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
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

    return lst_with_links, len(lst_with_links)
