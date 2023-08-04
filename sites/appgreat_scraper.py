#
#
#
#
# Company -> appgr8
# Link ----> https://www.appgr8.com/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time


session = requests.session()


def return_bs4_object(url: str) -> BeautifulSoup:
    '''
    Return bs4 object after simple request.
    '''
    return BeautifulSoup(session.get(url=url, headers=DEFAULT_HEADERS).text, 'lxml')


def get_data_from_site() -> list[dict]:
    '''
    ... get data from site with one requests.
    '''

    soup = return_bs4_object(url='https://www.appgr8.com/careers/')

    #
    soup_data = soup.find_all('a')

    lst_with_data = []
    for job in soup_data:
        if job:
            # check if 'positions' in job['href']
            if 'positions' in job['href']:

                data_soup = return_bs4_object(job['href'].strip())
                time.sleep(0.3)

                paragraf = data_soup.find('p').text

                if 'Bucharest' in paragraf or 'Romania' in paragraf:
                    title = data_soup.find('h4', attrs={'class': 'elementor-heading-title elementor-size-default'}).text
                    link = job['href']

                    lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "AppGreat",
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


company_name = 'AppGreat'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AppGreat',
                  'https://clutchco-static.s3.amazonaws.com/s3fs-public/logos/52175d74be34bfe849aef98e4ed36c4a.jpeg?VersionId=n87OrsHNyLbgXOo4MoyU4abLU4uoEUaV'))
