#
#
#
# Scraper Company - restartenergy
# link to this company ---> https://restartenergy.ro/cariere/
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
    Collect data from modal site.
    """

    response = requests.get(url='https://restartenergy.ro/cariere/',
                            headers=DEFAULT_HEADERS
                            )
    soup = BeautifulSoup(response.text, 'lxml')

    # data!
    soup_data = soup.find_all('div', class_='vc_tta-panel')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('h4', class_='vc_tta-panel-title vc_tta-controls-icon-position-left').find('a')['href']
        title = sd.find('span', class_='vc_tta-title-text').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://restartenergy.ro/cariere/' + link,
                "company": "restartenergy",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data, len(lst_with_data)
