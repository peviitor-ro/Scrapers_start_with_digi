#
#
#
# New scraper for peviitor.ro!
# Link to this jobs ---> https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_jumbo(url: str) -> list:
    """
    This func() return data from jumbo page.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('article', class_='x-control x-box x-article-box careers-article')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='title').text
        link = sd.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://corporate.e-jumbo.gr' + link,
            "company": "jumbo",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'jumbo'
data_list = get_data_from_jumbo('https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/')
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('jumbo',
                  'https://corporate.e-jumbo.gr/uploads/images/logo.png'
                  ))
