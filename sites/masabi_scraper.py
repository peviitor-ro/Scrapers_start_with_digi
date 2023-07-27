#
#
#
#
# Company -> Masabi
# Link ----> https://careers.masabi.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
from requests_html import HTMLSession
from bs4 import BeautifulSoup
#
import uuid
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


def collect_data_from_masabi() -> list[dict]:
    '''
    ... collect data with requests_html and configured headers.
    '''

    session = config_requests_html()
    response = session.get(url='https://careers.masabi.com/')
    sleep(1)

    # search data!
    data_job = response.html.render()
    print(data_job)

    session.close()


print(collect_data_from_masabi())
