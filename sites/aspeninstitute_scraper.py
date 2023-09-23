#
#
#
#
# Company -> aspeninstitute
# Link ----> https://aspeninstitute.ro/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_site():
    '''
    ... collect all data from site.
    '''

    response = requests.get(url='https://aspeninstitute.ro/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', attrs={'class': 'aspen-row-link'})

    lst_with_data = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('h3').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "AspenInstitute",
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


company_name = 'AspenInstitute'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AspenInstitute',
                  'https://www.aspeninstitute.org/wp-content/uploads/2020/11/aspen-institute-logo-white-on-blue-1920x1080-1.png'
                  ))
