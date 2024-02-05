#
#
#
#
# Company -> evalueserve
# Link-----> https://www.evalueserve.com/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import re


def collect_data_from_site():
    '''
    ... collect data with one request and default headers.
    '''

    response = requests.get(url='https://www.evalueserve.com/jobs/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # My method
    # levels = ['entry-level', 'mid-level', 'senior-level', 'leadership-level']
    # class_pattern = '|'.join(levels)
    # soup_data = soup.find_all('div', class_=re.compile(f'Romania ({class_pattern}) db-single-job-wrap'))

    # Rares -> method
    soup_data = soup.select("div[class$='Romania']")

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('div', attrs={'class': 'db-job-title'}).find('h4').text
        link = sd.find('div', attrs={'class': 'db-job-link'}).find('a')['href']
        city = sd.find('div', attrs={'class': 'db-location-country'}).find('h6').text.split(',')[0]

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "Evalueserve",
                    "country": "Romania",
                    "city": city
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Evalueserve'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Evalueserve',
                  'https://mltfwbciccuo.i.optimole.com/VDZzwSs-77A4qSCv/w:985/h:101/q:auto/https://www.evalueserve.com/wp-content/uploads/2021/10/Evalueserve__logo.svg'
                  ))
