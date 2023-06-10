#
#
#
# Start scrape Nasstar
# link -> https://nasstar.teamtailor.com/jobs?location=Bucharest&query=
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
    Collect data from one requests.
    """

    response = requests.get(
            url='https://nasstar.teamtailor.com/jobs?location=Bucharest&query=',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded')

    lst_with_data = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "nasstar",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_data, len(lst_with_data)
