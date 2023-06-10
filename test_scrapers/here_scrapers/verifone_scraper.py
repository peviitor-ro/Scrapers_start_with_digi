#
#
#
# Company - Verifone
# Link - https://www.verifone.com/en/careers/search?locations%5B%5D=8729&keyword=
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
    ... get data from verifone with one requests.
    """

    response = requests.get(url='https://www.verifone.com/en/careers/search?locations%5B%5D=8729&keyword=',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='views-row')

    lst_with_data = []
    for dt in soup_data:
        link = dt.find('span', class_='field-content').find('a')['href']
        title = dt.find('span', class_='field-content').find('a').find('span').text
        city = dt.find('div', class_='field-content').find('div').find('div').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "verifone",
            "country": "Romania",
            "city": city
            })

    return lst_with_data, len(lst_with_data)
