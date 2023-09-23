#
#
#
#
# Company ---> Azur
# Link -> https://www.azur.ro/ro/cariere
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_azur():
    '''
    ... collect data with one requests.
    '''

    response = requests.get(url='https://www.azur.ro/ro/cariere',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='titlu-sortare22')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a').text.strip()
        link = sd.find('a')['href'].strip()

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://www.azur.ro' + link,
                "company": "AZUR",
                "country": "Romania",
                "city": "Timisoara"
            })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'AZUR'
data_list = collect_data_from_azur()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('AZUR',
                  'https://www.azur.ro/images/logo.png'))
