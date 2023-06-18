#
#
#
# This is Scraper for AUSY
# Link to this Company ---> https://www.ausy.com/careers-ausy/all-our-jobs/romania/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
from random import randint


def collect_data_from_page(page: int) -> list:
    """
    This func() make post requests du AUSY.
    """

    response = requests.get(
            url=f'https://www.ausy.com/careers-ausy/all-our-jobs/romania/page-{page}/',
            headers=DEFAULT_HEADERS
        )
    soup = BeautifulSoup(response.content, 'lxml')
    soup_data = soup.find_all('li', class_='cards__item')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='cards__link')['href']
        title = sd.find('a', class_='cards__link').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.ausy.com' + link,
            "company": "ausy",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def scrape_all_data() -> list:
    """
    Scrape all data from AUSY.
    """

    page = 1
    flag = True

    lst_with_jobs = []
    while flag != False:

        data = collect_data_from_page(page)
        if len(data) > 0:
            lst_with_jobs.extend(data)
            print(f'Scrape {page}')
        else:
            flag = False
            print('Scraper do all job!')

        page += 1
        time.sleep(randint(1, 2))

    return lst_with_jobs


# update data on peviitor
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'ausy'
data_list = scrape_all_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ausy', 'https://www.ausy.com/sites/ausy-com/modules/custom/rbd_ausy_com/assets/img/logo.svg'))
