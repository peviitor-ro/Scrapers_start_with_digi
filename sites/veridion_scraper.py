#
#
#
# Scraper for Veridion Company
# Link to company career page -> https://veridion.com/careers/
#
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_veridion():
    '''
    ... this function collects all data and resturns a list with jobs
    '''

    response = requests.get('https://veridion.com/careers/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')


    soup_data = soup.find_all('div', class_='career-inner')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='fw-bold').text
        link = sd.find('div', class_='text-center careers-button-wrap w-100').find('a')['href']
        location = sd.find('h5', class_='light-grey').text.split()[0].replace("Bucharest","Bucuresti")

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "Veridion",
            "country": "Romania",
            "city": location
            })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Veridion'
data_list = collect_data_from_veridion()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Veridion',
                  'https://veridion.com/wp-content/themes/soleadify/assets/images/graphical-elements/main-logo.png'
                  ))






