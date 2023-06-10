#
#
#
# Scrape new Site -> ThreatConnect
# Link to this site -> https://jobs.lever.co/threatconnect?_ga=2.19358907.2008016264.1682672901-1880994929.1682672901
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper(url='https://jobs.lever.co/threatconnect?_ga=2.19358907.2008016264.1682672901-1880994929.1682672901'):
    """
    Return html data from ThreatConnect.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='posting')

    lst_with_jobs = []
    for sd in soup_data:
        link = sd.find('a', class_='posting-title')['href']
        title = sd.find('h5').text.strip()

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "threatconnect",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_jobs, len(lst_with_jobs)
