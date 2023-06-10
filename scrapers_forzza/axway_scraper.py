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


def get_data_from_site():
    '''
    Get data with one requests.
    '''

    response = requests.get('https://careers-axway.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-xs-12 title')

    lst_with_data = []
    for dt in soup_data:
        if 'href' in str(dt):
            title = dt.find('h2').text.strip()
            link = dt.find('a')['href'].strip()

            lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title,
                        "job_link":  link,
                        "company": "axway",
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


company_name = 'axway'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('axway',
                  'https://c-7055-20201030-www-axway-com.i.icims.com/themes/custom/axway2020/img/axway-logo-dark-gray.svg'
                  ))
