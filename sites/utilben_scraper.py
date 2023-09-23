#
#
#
#
# Company -> utilben -> Best
# Link ----> https://www.utilben.ro/careers#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
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


def collect_data_from_utilben():
    '''
    ... collect data with requests_html and configured headers.
    '''

    session = config_requests_html()
    response = session.get(url='https://www.utilben.ro/ajax/GetCareersPartial?categorySlug=')
    sleep(2)

    tr_elements = response.html.find('tr[style="vertical-align: middle !important;"]')

    lst_with_data = []
    for job in tr_elements:
        soup_bs4 = make_bs4_object(job.html)

        # here extract data
        title = soup_bs4.find('h3', attrs={'class': 'regular-title-small career-table-text'}).text
        link = soup_bs4.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "utilben",
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


company_name = 'utilben'
data_list = collect_data_from_utilben()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('utilben',
                  'https://www.utilben.ro/content/images/svg/utilben-logo.svg'
                  ))
