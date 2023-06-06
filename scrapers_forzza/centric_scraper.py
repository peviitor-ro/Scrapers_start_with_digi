#
#
#
# Company - centric
# Link -> https://careers.centric.eu/ro/open-positions/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_centric():
    """
    ... get data from centric with one requests.
    """

    response = requests.get(url='https://careers.centric.eu/ro/open-positions/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='card-grid__card-container')

    lst_with_data = []
    for dt in soup_data:

        job_data = dt.find('div', class_='card  default')

        if job_data:
            title = job_data.find('a').find('div',class_='card__wrapper').find('div',class_='card__title').text
            link = job_data.find('a')['href']
            city = dt.find('span', class_='tag__span').find('span').text

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "centric",
                "country": "Romania",
                "city": city
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'centric'
data_list = get_data_from_centric()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('centric',
                  'https://www.oribi.nl/cache/centric.2994/centric-s1920x1080.png'))
