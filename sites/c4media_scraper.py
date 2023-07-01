#
#
#
# Company -> c4media
# Link ----> https://c4media.com/career
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_c4media() -> list[dict]:
    '''
    ... collect data from c4media, with one requests.
    '''

    response = requests.get(url='https://c4media.com/career',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='items-center pb-4 m-auto mt-10 mb-4 border-b border-gray-300 md:flex')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a').text

        if 'Romania' in title:
            link = 'https://c4media.com' + sd.find('a')['href']

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "c4media",
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


company_name = 'c4media'
data_list = collect_data_from_c4media()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('c4media',
                  'https://c4media.com/_nuxt/img/c4media-logo.b690907.svg'))
