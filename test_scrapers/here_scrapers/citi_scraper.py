#
#
#
# Company - CITI !
# Link -> https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper() -> tuple:
    """
    Get data from websites.
    """

    response = requests.get(url='https://jobs.citi.com/search-jobs/Romania/287/2/798549/46/25/50/2',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a')

    lst_with_data = []
    for dt in soup_data:
        if 'job' in dt['href'] and dt.find('h2'):
            link = dt['href']
            title = dt.find('h2').text.strip()
            city = dt.find('span', class_='job-location').text.split(',')[0]

            # collect data
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://jobs.citi.com/' + link,
                    "company": "citi",
                    "country": "Romania",
                    "city": city
                })

    return lst_with_data, len(lst_with_data)
