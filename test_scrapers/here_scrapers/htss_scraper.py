#
#
#
# New scraper for HTSS
# link to company ---> https://ro.htssgroup.eu/cariere/
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
    Collect data from htss with only one request.
    """

    response = requests.get(
            url='https://ro.htssgroup.eu/cariere/',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='jobs__item')

    lst_with_data = []
    for sd in soup_data:
        link = sd['href'].strip()
        title = sd.text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "htssgroup",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data, len(lst_with_data)
