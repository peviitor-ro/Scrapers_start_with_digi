#
#
#
#
# Company -> spacelift
# Link ----> https://spacelift.io/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_spacelift():
    '''
    ... get all data with one requests.
    '''

    response = requests.get(url='https://spacelift.io/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', attrs={'class': 'CareersPage_jobItem__idxka'})

    lst_with_data = []
    for job in soup_data:
        title = job.find('p', attrs={'class': 'CareersPage_jobTitle__0AD3Y Typography_styleBase__bIYUB Typography_styleH6__9Ob_9'}).text
        link = job.find('a', attrs={'class': 'CareersPage_jobItemLink__okXue'})['href']

        if 'remote' in title.lower():
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "spacelift",
                    "country": "Romania",
                    "city": "Remote"
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'spacelift'
data_list = get_data_from_spacelift()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('spacelift',
                  'https://nachonacho.com/_next/image?url=https%3A%2F%2Ffiles.nachonacho.com%2Fusers%2Fcl5sl81dj20820508oehb13n81t%2Fnn_1658278209565_horizontal_dark_safetyArea.png&w=3840&q=75'
                  ))
