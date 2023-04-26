#
#
#
# Ursus scraper -> for peviitor.ro!
# Link to this site -> https://careers.asahiinternational.com/ursus-breweries/go/Joburile-disponibile-%C3%AEn-Ursus-Breweries/8560202/
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#


def set_headers():
    """
    This func() is about setting headers for scraping Ursus.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def get_data_reqeusts(url: str):
    """
    This func() make a post requests tu ursus.
    """

    response = requests.get(url=url, headers=set_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    # gat all data from tags
    data_soup = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for dt in data_soup:
        link = dt.find('a')['href']
        title = dt.find('a').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://careers.asahiinternational.com' + link,
            "company": "ursus",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def scrape_ursus():
    """
    This func() is about scrape ursus.
    """

    job_data = get_data_reqeusts('https://careers.asahiinternational.com/ursus-breweries/go/Joburile-disponibile-%C3%AEn-Ursus-Breweries/8560202/')

    with open('scrapers_forzza/data_ursus.json', 'w') as file_data:
        json.dump(job_data, file_data)

    print('Ursus ---> Done!')
