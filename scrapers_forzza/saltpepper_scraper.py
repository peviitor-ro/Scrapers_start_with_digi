#
#
#
# New Scraper for Salt and Pepper
# Link to this site -> https://saltandpepper.co/careers/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def default_headers():
    """
    For default headers for salt&pepper
    """
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
        }

    return DEFAULT_HEADERS


def collect_data_from_saltpepper():
    """
    This func() collect data from Salt & Pepper site.
    """

    response = requests.get('https://saltandpepper.co/careers/', headers=default_headers())
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('h3', class_='entry-title')

    lst_with_jobs = []
    for sd in soup_data:
        link = sd.find('a')['href']
        title = sd.find('a').text

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "saltandpepper",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'saltandpepper'
data_list = collect_data_from_saltpepper()
scrape_and_update_peviitor(company_name, data_list)
