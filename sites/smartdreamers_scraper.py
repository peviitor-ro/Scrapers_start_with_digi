#
#
#
#
# Company -> smartdreamers
# Link ----> https://www.smartdreamers.com/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_smartdreamers() -> list[dict]:
    '''
    ... get data from site with one requests.
    '''

    response = requests.get(url='https://www.smartdreamers.com/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'span12 widget-span widget-type-cell job-listing-simple'})

    lst_with_data = []
    for job in soup_data:
        link = job.find('a')['href']
        title = job.find('h3').text
        location = job.find('p').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "smartdreamers",
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


company_name = 'smartdreamers'
data_list = get_data_from_smartdreamers()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('smartdreamers',
                  'https://www.romanianstartups.com/wp-content/uploads/2015/06/smartdreamers-logo-176x100.png'
                  ))
