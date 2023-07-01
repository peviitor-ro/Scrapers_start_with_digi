#
#
#
# Scraper for Engie Company
# Link to company career page -> https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow=0
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
import time

def collect_data_from_engie() -> list[dict]:
    '''
    this function will collect all data and will return a list with jobs
    '''

    page_jobs = 0
    flag = True
    lst_with_data = []

    while flag != False:
        response = requests.get(url=f'https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow={page_jobs}', headers=DEFAULT_HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')

        soup_data = soup.find_all('tr', class_='data-row')

        if len(soup_data) > 1:
            for sd in soup_data:
                link = "https://jobs.engie.com" + sd.find('a')['href']
                title = sd.find('a').text

                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "Engie",
                    "country": "Romania",
                    "city": "Romania"
                })
        else:
            flag = False
            break
        page_jobs += 25
        time.sleep(1)
    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Engie'
data_list = collect_data_from_engie()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Engie',
                  "https://rmkcdn.successfactors.com/c4851ec3/1960b45a-f47f-41a6-b1c7-c.svg"
                  ))




