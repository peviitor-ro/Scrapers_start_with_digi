#
#
#
# New Scraper for peviitor.ro!
# link for this is ---> https://careers.egger.com/go/Jobs-in-Romania/8984955/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_data_from_site() -> list:
    """
    This func() return all data from this site. Jobs scrap.
    """

    response = requests.get(
            url='https://careers.egger.com/go/Jobs-in-Romania/8984955/',
            headers=DEFAULT_HEADERS
            )
    soup = BeautifulSoup(response.text, 'lxml')

    data_list = soup.find_all('tr', class_='data-row')

    lst_with_data = []
    for dl in data_list:
        link = dl.find('a')['href'].strip()
        title = dl.find('a').text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://careers.egger.com' + link,
            "company": "EGGER",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


# update data peviitor
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'EGGER'
data_list = get_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo(company_name,
                  'https://rmkcdn.successfactors.com/24f99312/dac140b7-bf0d-474e-b2c7-7.jpg'))
