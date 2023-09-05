#
#
#
# Scrape new Company - totalsoft
# links ---> https://careers.totalsoft.ro/professionals/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_totalsoft() -> list:
    """
    ... collect all data in one get requests.
    """

    response = requests.get(
            url='https://careers.totalsoft.ro/professionals/',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='job-item')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h2', class_='job-item_title').text.strip()
        link = sd.find('a')['href']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "totalsoft",
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


company_name = 'totalsoft'
data_list = collect_data_from_totalsoft()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('totalsoft',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/TotalSoft_logo.png/1200px-TotalSoft_logo.png'
                  ))
