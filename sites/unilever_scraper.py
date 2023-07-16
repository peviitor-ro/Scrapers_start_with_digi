#
#
#
#
# Company -> unilever
# Link ----> https://careers.unilever.com/romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_site() -> list[dict]:
    '''
    ... collect data with one requests.
    '''

    response = requests.get(url='https://careers.unilever.com/romania',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find('section', attrs={'class': 'job-list'}).find_all('li')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a')['href']
        title = sd.text.split('\n')[1]
        loc = sd.text.split('\n')[-2].split()[0].replace(',', '')

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://careers.unilever.com' + link,
                "company": "unilever",
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


company_name = 'unilever'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('unilever',
                  'https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/Unilever.svg/1200px-Unilever.svg.png'
                  ))
