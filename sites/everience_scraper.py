#
#
#
# Company - everience
# link - https://everience.jobs.net/jobs?posted=&radius=&cb_apply=false&keywords=&location=&pay=&emp=&company=&cityStateFacet=&categoryFacet=all
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_site() -> list:
    '''
    ... get data with one requests.
    '''

    response = requests.get(url='https://everience.jobs.net/jobs?posted=&radius=&cb_apply=false&keywords=&location=&pay=&emp=&company=&cityStateFacet=&categoryFacet=all',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='data-results-content-parent relative')

    lst_with_data = []
    for dt in soup_data:
        link = dt.find('a')['href']
        title = dt.find('div', class_='data-results-title dark-blue-text b').text
        location = dt.find('div', class_='data-details').find('span').text.split()[0].replace(',', '')

        if location.lower() == 'timișoara' or location.lower() == 'bucurești' or location.lower() == 'romania':
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": 'https://everience.jobs.net/' + link,
                    "company": "everience",
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


company_name = 'everience'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('everience',
                  'https://www.everience.com/wp-content/uploads/2022/08/cropped-Everience-logo-final.png'
                  ))
