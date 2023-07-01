#
#
#
# Company -> neptun-gears
# Link ----> http://www.neptun-gears.ro/ro/cariere/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_neptungears() -> list[dict]:
    '''
    ... collect data with one requests.
    '''

    response = requests.get(url='http://www.neptun-gears.ro/ro/cariere/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('ul')[-7]

    lst_with_data = []
    for sd in soup_data:
        data = sd.find('a')

        if data != -1:
            link = data['href']
            title = data.text

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "NeptunGears",
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


company_name = 'NeptunGears'
data_list = collect_data_from_neptungears()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('NeptunGears',
                  'http://www.neptun-gears.ro/images/logo.jpg'
                  ))
