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


def collect_data_from_page(page: int):
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
            "company": "AUSY",
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


company_name = 'AUSY'
data_list = scrape_all_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AUSY', 'https://cdn.cookielaw.org/logos/9c9e1da5-cb5e-4789-be00-8f37c0e84ef3/62e61997-de64-46c2-bd04-cd5f54c2ff86/54e09e2b-769b-4b50-aad3-12e44849e0ff/ausy_logo-removebg-preview.png'))
