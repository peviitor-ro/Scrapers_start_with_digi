#
#
#  This file contains the Requests + BS4 shorts;
#  Avoid DRY code, its not a good practice!!!
#  Make Python3 better place for code!
#
#  Start here!
#
#
import requests
from bs4 import BeautifulSoup
#
from .default_headers import DEFAULT_HEADERS


# Global Session -> avoid multiple requests
# ... and all classes can use it in one script
session = requests.Session()


class GetStaticSoup:
    '''
    ... This class return soup object from static page!
    '''

    def __new__(cls, link, custom_headers=None):

        headers = DEFAULT_HEADERS.copy()

        #  if user have custom headers,
        #  update the headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # return soup object from static page
        return BeautifulSoup(response.content, 'lxml')


class GetRequestJson:
    '''
    ... This class return JSON object from get requests!
    '''

    def __new__(cls, link, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Dacă utilizatorul are headere personalizate, actualizează headerele
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # Parse response to JSON and return ditct oject
        try:
            json_response = response.json()
            return json_response
        except ValueError as e:
            print(f"Errors. No JSON! Details: {e}")
            return None


class PostRequestJson:
    '''
    ... This class return JSON object from post requests!
    '''

    def __new__(cls, url, custom_headers=None, data_raw=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        response = session.post(url, headers=headers, data=data_raw)

        # Parse response to JSON or to soup object
        try:
            json_response = response.json()
            return json_response
        except ValueError as e:
            pass

        # second try
        try:
            html_response = response.text
            return BeautifulSoup(html_response, 'lxml')
        except ValueError as e:
            pass


class GetHtmlSoup:
    '''
    ... method if server return html response,
    after post requests.
    '''

    def __new__(cls, html_response):
        return BeautifulSoup(html_response, 'lxml')


class GetHeadersDict:
    '''
    ... method if server return headers response,
    after session.headers
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers).headers

        return response
