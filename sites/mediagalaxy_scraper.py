#
#
#
# Scraper for Mediagalaxy Company
# Link to company career page -> https://mediagalaxy.ro/cariere/
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

def collect_data_from_mediagalaxy():
    '''
    ... this function will collect data and will return a list with jobs
    '''

    response = requests.get(url='https://mediagalaxy.ro/cariere/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='border rounded px-8')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='flex-shrink-0 mb-3 md:mb-0 md:w-64 md:pr-6 font-medium capitalize').text
        new_title = title.capitalize()
        link = title.split()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": "https://mediagalaxy.ro/cariere/#" + "-".join(link),
            "company": "Mediagalaxy",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Mediagalaxy'
data_list = collect_data_from_mediagalaxy()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Mediagalaxy',
                  "https://bucurestimall.ro/wp-content/uploads/2016/12/MediaGalaxy.jpg"
                  ))

