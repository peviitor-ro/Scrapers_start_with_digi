#
#
#
# Company -> coremaker
# Link -> https://coremaker.io/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_site() -> list[dict]:
    '''
    ... get data with one requests.
    '''

    response = requests.get(url='https://coremaker.io/careers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4'})

    lst_with_data = []
    for dt in soup_data:
        link = 'https://coremaker.io' + dt.find('a')['href']
        title = dt.find('h5').text
        location = dt.find('span', attrs={'class': 'MuiTypography-root jss43 MuiTypography-caption'}).text.split()[-1]

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "coremaker",
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


company_name = 'coremaker'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('coremaker',
                  'https://content.ejobs.ro/img/logos/3/318001.png'))
