#
#
#
# New scraper for Emia company!
# Link ---> https://emia.com/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_emia() -> list:
    """
    Collect all data from Emia, with one requests.
    """

    response = requests.get(url='https://emia.com/jobs/',
                            headers=DEFAULT_HEADERS
                            )
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-lg-4 col-md-6 pt--30')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='card-job top-only')['href']
        title = sd.find('h5', class_='h5').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "emia",
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


company_name = 'emia'
data_list = collect_data_from_emia()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('emia',
                  'https://emia.com/image/emia-logo.png'
                  ))
