#
#
#
# Company - ninedots
# Link - https://ninedots.io/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper() -> tuple:
    """
    ... get remote data for Roumania.
    """

    response = requests.get(url='https://ninedots.io/jobs/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    #
    soup_data = soup.find_all('a', class_='job-card')

    lst_with_data = []
    for dt in soup_data:
        link = 'https://ninedots.io' + dt['href']
        title = dt.find('h3').text
        location = dt.find('div', class_='info location').find('p').text.split()[0].replace(',', '')

        if 'remote' in location.lower():
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "ninedots",
                    "country": "Romania",
                    "city": location
                })

    return lst_with_data, len(lst_with_data)
