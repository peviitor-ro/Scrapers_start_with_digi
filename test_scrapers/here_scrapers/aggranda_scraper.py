#
#
#
# Company -> aggranda
# Link -> https://www.aggranda.com/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper() -> list:
    '''
    ... get data with one requests.
    '''

    response = requests.get(url='https://www.aggranda.com/jobs/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='content_job_container')

    lst_with_data = []
    for dt in soup_data:
        link = dt.find('a')['href']
        title = dt.find('h4').text
        city = dt.find('div', class_='job_location').find('h6').text
        #
        # try to clear city data and link!
        if len(city.split()) > 1:
            city = city.split()[0].replace(',', '')
        if 'https://www.aggranda.com' not in link:
            link = 'https://www.aggranda.com' + link

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "aggranda",
            "country": "Romania",
            "city": city
            })

    return lst_with_data, len(lst_with_data)
