#
#
#
# Scraper for Codezilla Company
# Link to company career page -> https://codezilla.global/jobs
#
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_codezilla() -> list[dict]:
    '''
    ... this function collects all data and returns a list with jobs
    '''

    response = requests.get('https://codezilla.global/jobs', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='JobListing_certified_inner__naKv8 certified')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h3').text
        link = "https://codezilla.global" + sd.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Codezilla",
            "country": "Romania",
            "city": "Remote"
        })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Codezilla'
data_list = collect_data_from_codezilla()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Codezilla',
                  "https://api.codezilla.ro/uploads/logo_black_03bc39c300.png"
                  ))
