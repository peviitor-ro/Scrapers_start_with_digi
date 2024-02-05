#
#
#  This file contains the Requests + BS4 shorts;
#  Avoid DRY code, its not a good practice!!!
#  Make Python3 better place for code!
#
#  Start here!
#
# Note ---> Update certifi for bad SSL
# if SSL invalid ---> rezolve without error in terminal
# ... plus sa fac aceeasi chestie ca la PostRequestJson si in GetRequestJson
#
import requests
from bs4 import BeautifulSoup
#
import cfscrape
#
from .default_headers import DEFAULT_HEADERS
#
import xml.etree.ElementTree as ET


# Global Session -> avoid multiple requests
# ... and all classes can use it in one script
session = requests.Session()


class GetStaticSoup:
    '''
    ... This class return soup object from static page!
    '''

    def __new__(cls, url, custom_headers=None):

        headers = DEFAULT_HEADERS.copy()

        #  if user have custom headers,
        #  update the headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers)

        # return soup object from static page
        return BeautifulSoup(response.text, 'lxml')


class GetRequestJson:
    '''
    ... This class return JSON object from get requests!
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Dacă utilizatorul are headere personalizate, actualizează headerele
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers)

        # Parse response to JSON and return ditct oject
        try:
            json_response = response.json()
            return json_response
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


class PostRequestJson:
    '''
    ... This class return JSON object from post requests!
    '''

    def __new__(cls, url, custom_headers=None, data_raw=None, data_json=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        if data_json:
            response = session.post(url, headers=headers, json=data_json)
        else:
            response = session.post(url, headers=headers, data=data_raw)

        try:
            return response.json()
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


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

        response = session.head(url, headers=headers).headers

        return response


class HackCloudFlare:
    '''
    ... this method can help you avoid CloudFlare protection.
    Is not a hack, but useful tool.
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if headers is requiered
        if custom_headers:
            headers.update(custom_headers)

        scraper = cfscrape.create_scraper()

        return BeautifulSoup(scraper.get(url).content, 'lxml')


class GetXMLObject:
    '''
    ... this class will return data from XML stored in a list
    '''
    
    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if custom headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return ET.fromstring(response.text)
