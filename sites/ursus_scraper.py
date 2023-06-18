#
#
#
# Ursus scraper -> for peviitor.ro!
# Link to this site -> https://careers.asahiinternational.com/ursus-breweries/go/Joburile-disponibile-%C3%AEn-Ursus-Breweries/8560202/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_reqeusts(url: str):
    """
    This func() make a post requests tu ursus.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
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


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'ursus'
data_list = get_data_reqeusts('https://careers.asahiinternational.com/ursus-breweries/go/Joburile-disponibile-%C3%AEn-Ursus-Breweries/8560202/')
scrape_and_update_peviitor(company_name, data_list)
