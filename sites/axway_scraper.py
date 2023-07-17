#
#
#
# Company -> axway
# Link -> https://careers-axway.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest&mobile=false&width=1268&height=500&bga=true&needsRedirect=false&jan1offset=120&jun1offset=180
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
from time import sleep


def get_data_from_site():
    '''
    Get data with one requests.
    '''

    response = requests.get('https://careers-axway.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest',
                            headers=DEFAULT_HEADERS)
    #
    sleep(3)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'row'})

    lst_with_data = []
    for dt in soup_data:
        print(dt)
        title = dt.find('h2').text.strip()
        link = dt.find('a')['href'].strip()

        lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "axway",
                    "country": "Romania",
                    "city": "Bucharest"
               })

    return lst_with_data


print(get_data_from_site())
