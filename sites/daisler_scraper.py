#
#
#
# New scraper for Daisler House
# Link t0 scrape ---> https://www.daisler.ro/despre-noi/cariere
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_daisler():
    """
    This func() collect data from Daisler.
    ... func() have default headers.
    """

    response = requests.get('https://www.daisler.ro/despre-noi/cariere', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='item-details')

    lst_with_jobs = []
    for sd in soup_data:
        title = sd.find('h2').text
        link = sd.find('a')['href']

        lst_with_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "daisler",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'daisler'
data_list = collect_data_from_daisler()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('daisler', 'https://www.daisler.ro/skin/frontend/daisler/default/images/logo.png'))
