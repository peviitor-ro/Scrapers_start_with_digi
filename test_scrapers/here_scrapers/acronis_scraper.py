#
#
#
# New scraper for -> Acronis
# Acronis job page -> https://www.acronis.com/en-eu/careers/jobs/
# Acronis API for scraping -> https://boards.greenhouse.io/acronis
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
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://boards.greenhouse.io/acronis',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='opening')

    lst_with_data = []
    for dt in soup_data:

        # check if Romania in location
        location = dt.find('span', class_='location').text
        if 'Romania' in location or 'România' in location:
            link = dt.find('a')['href']
            title = dt.find('a').text

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://boards.greenhouse.io/' + link,
                    "company": "acronis",
                    "country": "Romania",
                    "city": location.split(', ')[0]
                })

    return lst_with_data, len(lst_with_data)
