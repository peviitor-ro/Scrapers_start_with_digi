#
#
#
#
# Company -> jivygroup
# Link ----> https://www.jivygroup.com/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_jivy() -> list[dict]:
    '''
    ... collect data with one request and default headers.
    '''

    response = requests.get(url='https://www.jivygroup.com/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('article')

    lst_with_data = []
    for job in soup_data:
        data = job.find('a', attrs={'class': 'eael-grid-post-link'})

        if data:
            title = data.text
            link = data['href']

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "jivygroup",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'jivygroup'
data_list = collect_data_from_jivy()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('jivygroup',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlQgdFvj__TQcluuKMKggStP5KR-x31rZioEWTM1bhCA&s'
                  ))
