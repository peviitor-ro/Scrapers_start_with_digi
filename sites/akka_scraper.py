#
#
#
#  Company - > aKKa
# Link -> https://www.akka-technologies.com/people-careers/jobs-list/?job_l%5B%5D=job_location_en_161&job_order=date&search=&ajax=true&job_p=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
from math import ceil


def get_soup_object(page: str):
    '''
    ... return BeautifiuSoup object.
    '''

    response = requests.get(url=f'https://www.akka-technologies.com/people-careers/jobs-list/?job_l%5B%5D=job_location_en_161&job_order=date&search=&ajax=true&job_p={page}',
                            headers=DEFAULT_HEADERS)
    return BeautifulSoup(response.text, 'lxml')


def get_data_from_akka() -> list[dict]:
    '''
    ... return data from site in json format.
    '''

    page = get_soup_object('1')
    page_n = page.find('div', attrs={'class': 'cell-6 total-job-result tag'}).text.split()[0]

    if page_n:
        page_n = ceil(int(page_n) / 20)

    lst_with_data = []
    for dt in range(1, page_n + 1):

        soup = get_soup_object(str(dt))
        soup_data = soup.find_all('div', attrs={'class': 'job-item js-jobitem'})

        for data in soup_data:
            link = data.find('a')['href']
            title = data.find('h3').text
            location = data.find('div', attrs={'class': 'job-items-infos'}).find_all('p')[1].text.split()[-1]

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "akka",
                "country": "Romania",
                "city": location
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'akka'
data_list = get_data_from_akka()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('akka',
                  'https://www.akka-technologies.com/app/themes/akka/static/img/logo.svg'
                  ))
