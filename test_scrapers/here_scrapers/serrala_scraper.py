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


def run_scraper() -> tuple:
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

    return lst_with_data, len(lst_with_data)
