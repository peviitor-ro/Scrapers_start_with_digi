#
#
#
#
# Company -> RomSoft
# Link ----> https://www.rms.ro/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_romsoft() -> list[dict]:
    '''
    ... collect data from romsoft with one requests.
    '''

    response = requests.get(url='https://www.rms.ro/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='awsm-list-left-col')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='awsm-job-post-title').find('a').text
        link = sd.find('h2', class_='awsm-job-post-title').find('a')['href']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "RomSoft",
                "country": "Romania",
                "city": "Remote"
                })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'RomSoft'
data_list = collect_data_from_romsoft()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('RomSoft',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2pJJUnXx4Bx5gJ8KiQfZdkOwndZcPOt_yC_UucjBDzg&s'))
