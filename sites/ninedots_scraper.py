#
#
#
# Company - ninedots
# Link - https://ninedots.io/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_remote_data() -> list:
    """
    ... get remote data for Roumania.
    """

    response = requests.get(url='https://ninedots.io/jobs/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    #
    soup_data = soup.find_all('a', class_='job-card')

    lst_with_data = []
    for dt in soup_data:
        link = 'https://ninedots.io' + dt['href']
        title = dt.find('h3').text
        location = dt.find('div', class_='info location').find('p').text.split()[0].replace(',', '')

        if 'remote' in location.lower():
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "ninedots",
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


company_name = 'ninedots'
data_list = get_remote_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ninedots',
                  'https://pbs.twimg.com/profile_images/1562739566326566912/63KhdH9X_400x400.jpg'
                  ))
