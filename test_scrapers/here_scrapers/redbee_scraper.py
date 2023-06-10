#
#
#
# New scraper for Redbee
# Link for this scraper is -> https://redbeesoftware.com/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper(url='https://redbeesoftware.com/careers/') -> tuple:
    """
    This func() return all jobs from redbee.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    soup_data = soup.find_all('div', class_='elementor-widget-wrap elementor-element-populated')

    lst_with_data = []
    for sd in soup_data:

        try:
            link = sd.find('a')['href']
        except:
            link = ''

        try:
            title = sd.find('p').text
        except:
            title = ''

        if title != '':
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "redbee",
                "country": "Romania",
                "city": "Romania"
                })

    return lst_with_data, len(lst_with_data)
