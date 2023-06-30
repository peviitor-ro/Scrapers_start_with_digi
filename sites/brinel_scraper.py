# Scraper for Brinel Company
# Link to company career page -> https://www.brinel.ro/cariere
#
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_brinel() -> list[dict]:
    '''
    this function will retrieve all the data for all jobs
    '''

    response = requests.get(url='https://www.brinel.ro/cariere', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-md-4 col-sm-6')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h6').find('a').text
        link = "https://www.brinel.ro" + sd.find('h6').find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Brinel",
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


company_name = 'Brinel'
data_list = collect_data_from_brinel()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Brinel',
                  "https://www.brinel.ro/typo3conf/ext/brinel_pack/Resources/Public/img/brinel_tagline.png"
                  ))
