#
#
#
#
# Company -> leadlion
# Link ----> https://leadlion.ro/cariere/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_leadlion() -> list[dict]:
    '''
    ... collect data from leadlion with one requests
    with default headers.
    '''

    res = requests.get(url='https://leadlion.ro/cariere/',
                       headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'vc_row wpb_row vc_inner vc_row-fluid job-single vc_custom_1652085815545 vc_row-has-fill'})

    lst_with_data = []
    for job in soup_data:
        title = job.find('h3', attrs={'class': 'title'}).text.strip()
        link = job.find('a')['href']

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "leadlion",
                    "country": "Romania",
                    "city": "Bucuresti"
                    })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'leadlion'
data_list = collect_data_from_leadlion()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('leadlion',
                  'https://leadlion.ro/wp-content/uploads/2020/09/logo-black-2.png'
                  ))
