#
#
#
#
# Company -> corteva
# Link ----> https://careers.corteva.com/job-search-results/?keyword=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
from requests_html import HTMLSession
from bs4 import BeautifulSoup
#
import uuid
#
from time import sleep


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


def collect_data_from_corteva():
    '''
    ... collect data.
    '''

    session = config_requests_html()
    response = session.get(url='https://careers.corteva.com/job-search-results/?keyword=Romania')
    sleep(1)

    response.html.render()
    tr_elements = response.html.find('div.jobTitle')

    lst_with_data = []
    for job in tr_elements:
        soup_bs4 = make_bs4_object(job.html)

        title = soup_bs4.find('a').text
        link = 'https://careers.corteva.com' + soup_bs4.find('a')['href']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "Corteva",
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


company_name = 'Corteva'
data_list = collect_data_from_corteva()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Corteva',
                  'https://download.logo.wine/logo/Corteva/Corteva-Logo.wine.png'))
