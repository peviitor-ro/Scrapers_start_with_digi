#
#
#
# New scraper for company - intersnack
# Link to this company ---> https://www.intersnack.ro/cariere/oportunitati-de-cariera
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
    Collect all data from intersnack... all jobs.
    """

    response = requests.get(
            url='https://www.intersnack.ro/cariere/oportunitati-de-cariera',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='ce__isnack-teaserpillar-teaser-item bg__isnack bg__isnack-red')

    list_with_data = []
    for sd in soup_data:
        link = sd.find('div', class_='d-flex justify-content-center ce__isnack-teaserpillar-teaser-btn').find('a')['href']
        title = sd.find('h2', class_='text-center font__is').text

        list_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://www.intersnack.ro/' + link,
                "company": "intersnack",
                "country": "Romania",
                "city": "Romania"
                })

    return list_with_data, len(list_with_data)
