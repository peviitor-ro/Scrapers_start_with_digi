#
#
#
# New Scraper for uniqasoftware
# Link to this site - https://www.uniqasoftware.ro/join-uss/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_uniqa() -> list:
    """
    General func() for collect data.
    """

    response = requests.get(url='https://www.uniqasoftware.ro/join-uss/jobs/',
                            headers=DEFAULT_HEADERS
                            )
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('div', class_='col-lg-4 col-md-6 col-sm-12')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('div', class_='job-link').find('a')['href']
        title = sd.find('div', class_='job-name').text

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "uniqasoftware",
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


company_name = 'uniqasoftware'
data_list = collect_data_from_uniqa()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('uniqasoftware', 'https://www.uniqasoftware.ro/wp-content/uploads/2021/04/120x60.jpeg'))
