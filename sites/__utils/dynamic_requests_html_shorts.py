#
#
#
#  File with shorts for render JS pages!
#  Use requests_html for dynamic rendering;
#
#
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from .default_headers import DEFAULT_HEADERS


class GetDynamicSoup:
    '''
    ... This class returns soup object from dynamic pages using requests_html!
    '''

    def __new__(cls, link, custom_headers=None):

        session = HTMLSession()

        headers = DEFAULT_HEADERS.copy()

        #  if user has custom headers,
        #  update the headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # Render Dynamic page with JS
        response.html.render()

        # return soup object from dynamic page
        return BeautifulSoup(response.html.html, 'lxml')
