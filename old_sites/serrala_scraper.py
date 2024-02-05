#
#
#
# Company - serrala
# link -> https://careers.serrala.com/search/?q=&q2=&alertId=&locationsearch=&geolocation=&searchby=distance&d=10&lat=&lon=&title=&facility=&location=RO
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_serrala() -> list:
    '''
    Get data with one requests.
    '''

    response = requests.get(url='https://careers.serrala.com/search/?q=&q2=&alertId=&locationsearch=&geolocation=&searchby=distance&d=10&lat=&lon=&title=&facility=&location=RO',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    #
    soup_data = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for dt in soup_data:
        link = dt.find('a', class_='jobTitle-link')['href']
        title = dt.find('a', class_='jobTitle-link').text
        city = dt.find('span', class_='jobLocation').text.strip().split()[0].replace(',', '')

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://careers.serrala.com' + link,
            "company": "serrala",
            "country": "Romania",
            "city": city
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'serrala'
data_list = get_data_serrala()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('serrala',
                  'https://www.serrala.com/themes/custom/serrala/assets/images/serrala-logo-ruby.svg'
                  ))
