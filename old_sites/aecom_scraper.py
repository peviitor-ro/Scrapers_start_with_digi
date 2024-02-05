#
#
#
#
# Company -> AECOM
# Link ----> https://aecom.jobs/rom/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


session = requests.Session()


def collect_data_from_aecom():
    '''
    ... collect data with one request and default headers.
    '''

    # data to store
    lst_with_data = []

    flag = True
    offset = 0
    while flag:
        response = session.get(f'https://aecom.jobs/rom/jobs/ajax/joblisting/?num_items=15&offset={offset}',
                               headers=DEFAULT_HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')

        soup_data = soup.find_all('li', class_='direct_joblisting with_description')

        if len(soup_data) < 1:
            flag = False

        # here extrat data from each job
        for job in soup_data:
            loc = job.find('div', class_='direct_joblocation').text.strip()

            if 'romania' not in loc.lower():
                break

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job.find('h4').text.strip(),
                    "job_link": 'https://aecom.jobs/' + job.find('a').get('href').strip(),
                    "company": "AECOM",
                    "country": "Romania",
                    "city": loc.split('\n')[0]
                })

        offset += 15

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'AECOM'
data_list = collect_data_from_aecom()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AECOM',
                  'https://1000logos.net/wp-content/uploads/2021/12/AECOM-logo.png'))
