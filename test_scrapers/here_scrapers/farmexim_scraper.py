#
#
#
# New Scraper for Pirelli!
# Link for this job page ---> https://www.farmexim.ro/posturi-vacante-26.html
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper(url='https://www.farmexim.ro/posturi-vacante-26.html') -> tuple:
    """
    Collect data from farmexim. All data from this site in one lst with dicts.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='service-block-desc')

    lst_with_jobs = []
    for data in soup_data:
        link = data.find('a')['href']
        title = data.find('a').text.strip()

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.farmexim.ro' + link,
            "company": "farmexim",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_jobs, len(lst_with_jobs)
