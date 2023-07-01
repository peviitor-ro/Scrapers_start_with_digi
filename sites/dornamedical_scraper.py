#
#
#
# Company -> DornaMedical
# Link ----> https://www.dornamedical.ro/cariere/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_dornamedical() -> list[dict]:
    '''
    ... collect data with one requests.
    '''

    response = requests.get(url='https://www.dornamedical.ro/cariere/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('h2', class_='entry-title')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a')['href']
        title = sd.find('a').text.strip()

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "DornaMedical",
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


company_name = 'DornaMedical'
data_list = collect_data_from_dornamedical()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('DornaMedical',
                  'https://www.dornamedical.ro/wp-content/uploads/2022/04/logo-2-culori.png'))
