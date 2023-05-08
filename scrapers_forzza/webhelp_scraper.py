#
#
#
# New Scraper for WebHelp
# Link to this company jobs ---> https://job.webhelp.ro/ro/offre-emploi?job=0&city=0&sector=0&language=0&page=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
from random import randint


def collect_data_from_webhelp(num: int) -> list:
    """
    Collect data from webHelp.
    """

    response = requests.get(
            url=f'https://job.webhelp.ro/ro/offre-emploi?job=0&city=0&sector=0&language=0&page={num}', 
            headers=DEFAULT_HEADERS
        )
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('div', class_='poste content-gray-box')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('h5').find('a')['href']
        title = sd.find('h5').find('a').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://job.webhelp.ro' + link,
            "company": "webhelp",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def scrape_all_data_from_webhelp() -> list:
    """
    Scrape all data from Webhelp.
    """

    page = 1
    flag = True

    lst_with_jobs = []
    while flag != False:

        data = collect_data_from_webhelp(page)
        if len(data) > 0:
            lst_with_jobs.extend(data)
            print(f'Scrape page {page}')
        else:
            print('Scraper do all job!')
            flag = False

        page += 1
        time.sleep(randint(1, 2))

    return lst_with_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'webhelp'
data_list = scrape_all_data_from_webhelp()
scrape_and_update_peviitor(company_name, data_list)
