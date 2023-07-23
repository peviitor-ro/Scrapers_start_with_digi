#
#
#
# New scraper for Orion Company
# Link to this Company ---> https://www.orioninc.com/careers/jobs/?_job_location=romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_orion() -> list:
    """
    ...collect data from site. From hidden post request.
    """

    response = requests.get(url='https://www.orioninc.com/careers/jobs/?_job_location=romania',
                            headers=DEFAULT_HEADERS
                            )
    soup = BeautifulSoup(response.text, 'lxml')

    # data from here
    soup_data = soup.find_all('article', class_='teaser teaser-search col-12')

    lst_with_data = []
    for sd in soup_data:

        link = sd.find('a', class_='article-title')['href']
        title = sd.find('a', class_='article-title').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://www.orioninc.com' + link,
            "company": "orionic",
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


company_name = 'orionic'
data_list = collect_data_from_orion()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('orionic', 'https://www.orioninc.com/wp-content/themes/orion/dist/images/orion_innovation_logo_white.svg'))
