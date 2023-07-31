#
#
#
#
# Company -> Aecom
# Link ----> https://aecom.jobs/rom/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
from math import ceil


session = requests.Session()


def return_soup(url: str) -> BeautifulSoup:
    '''
    ... this function return soup object.
    '''

    response = session.get(url=url, headers=DEFAULT_HEADERS)

    return BeautifulSoup(response.text, 'lxml')



def collect_data_from_aecom() -> list[dict]:
    '''
    ... collect data with one request and default headers.
    '''

    num_jobs = return_soup(url='https://aecom.jobs/jobs/?location=Romania&r=25').find('h3', attrs={'class': 'direct_highlightedText'}).text.strip().split()[0]

    # time to count for loop!
    diez_num_url = ceil(int(num_jobs) / 15) - 1

    # return nums of jobs
    soup = return_soup(url=f'https://aecom.jobs/jobs/?location=Romania&r=25#{diez_num_url}')
    soup_data = soup.find_all('li', attrs={'class': 'direct_joblisting with_description'})

    lst_with_data = []
    for job in soup_data:
        title = job.find('h4').text.strip()
        link = 'https://aecom.jobs' + job.find('a')['href'].strip()
        loc = job.find('div', attrs={'class': 'direct_joblocation'}).text.split()[0].replace(',', '')

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "aecom",
                    "country": "Romania",
                    "city": loc
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'aecom'
data_list = collect_data_from_aecom()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('aecom',
                  'https://1000logos.net/wp-content/uploads/2021/12/AECOM-logo.png'))
