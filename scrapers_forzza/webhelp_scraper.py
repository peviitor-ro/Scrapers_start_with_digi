#
#
#
# New Scraper for WebHelp
# Link to this company jobs ---> https://jobs.webhelp.com/job-search/?keyword=&country=Romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#


def collect_data_from_webhelp() -> list:
    """
    Collect data from webHelp.
    """

    response = requests.get(
            url=f'https://jobs.webhelp.com/job-search/?keyword=&country=Romania',
            headers=DEFAULT_HEADERS
        )
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('div', class_='job')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a')['href']
        title = sd.find('h3').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "webhelp",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'webhelp'
data_list = collect_data_from_webhelp()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('webhelp',
                  'https://jobs.webhelp.com/wp-content/themes/jobswh/img/logo.svg'
                  ))
