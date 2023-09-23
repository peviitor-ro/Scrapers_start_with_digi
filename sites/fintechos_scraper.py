#
#
#
#
# Company -> fintechos
# Link ----> https://fintechos.com/careers/openings/
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
    ... get all data with one requests to this site.
    '''

    response = requests.get(url='https://fintechos.com/careers/openings/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='opening')

    lst_with_data = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('h3', class_='opening--title').text
        city = sd.find('div', class_='opening--data__location').find('p').text

        if city == 'Bucharest':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "fintechos",
                "country": "Romania",
                "city": 'Bucuresti'
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'fintechos'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('fintechos',
                  'https://7569749.fs1.hubspotusercontent-na1.net/hubfs/7569749/Typequast-fintechOS.png'
                  ))
