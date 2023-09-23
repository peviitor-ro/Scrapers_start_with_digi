#
#
#
# Company: Hosterion
# Link -> https://hosterion.ro/cariere/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_hosterion():
    '''
    ... collect data with one requests.
    '''

    response = requests.get(url='https://hosterion.ro/cariere/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find('div', class_='content-column')

    lst_with_data = []
    for sd in soup_data.find_all('li'):
        link = sd.find('a')['href']
        title = sd.find('a').text

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "hosterion",
                    "country": "Romania",
                    "city": "Romania"
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'hosterion'
data_list = collect_data_from_hosterion()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hosterion',
                  'https://hosterion.ro/blog/wp-content/uploads/2016/11/hosterion_small_logo.jpg'
                  ))
