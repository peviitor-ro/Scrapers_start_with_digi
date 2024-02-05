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


def collect_data_from_intersnack() -> list:
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

    return list_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'intersnack'
data_list = collect_data_from_intersnack()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('intersnack',
                  'https://www.intersnack.ro/typo3conf/ext/udg_package/Resources/Public/Images/SVG/intersnackgroup.svg'
                  ))
