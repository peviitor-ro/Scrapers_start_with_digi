#
#
#
# Company -> axway
# Link -> https://careers-axway.icims.com/jobs/search?ss=1&searchLocation=13526--Bucharest&mobile=false&width=1268&height=500&bga=true&needsRedirect=false&jan1offset=120&jun1offset=180
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
from requests_html import HTMLSession
from bs4 import BeautifulSoup
#
from time import sleep
import uuid


def make_bs4_object(requests_html_object) -> BeautifulSoup:
    '''
    Convert requests-html to bs4 object.
    '''

    return BeautifulSoup(requests_html_object, 'lxml')


def config_requests_html() -> HTMLSession:
    '''
    Config requests_html with headers and make new requests
    and parse js data.
    '''

    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    session.headers['Accept-Language'] = 'en-US,en;q=0.5'
    session.headers['Refer'] = 'https://google.com'
    session.headers['DNT'] = '1'

    return session


def collect_data_from_axway() -> list[dict]:
    '''
    ... collect data with requests_html and configured headers.
    '''

    session = config_requests_html()
    response = session.get(url='https://careers-axway.icims.com/jobs/search?ss=1&in_iframe=1&searchLocation=13526--Bucharest')
    sleep(2)

    # scrape data!
    lst_with_data = []
    data = response.html.find('div.row')
    for job in data:
        soup_bs4 = make_bs4_object(job.html)

        # here extract data!
        link = soup_bs4.find('a', attrs={'class': 'iCIMS_Anchor'})
        title = soup_bs4.find('h2')

        if link and title:
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title.text.strip(),
                    "job_link": link['href'],
                    "company": "Axway",
                    "country": "Romania",
                    "city": "Bucharest"
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Axway'
data_list = collect_data_from_axway()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Axway',
                  'https://c-7055-20201030-www-axway-com.i.icims.com/themes/custom/axway2020/img/axway-logo-dark-gray.svg'
                  ))
