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
            url='https://totalsoft.applytojob.com/apply/',
            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', attrs={'class': 'list-group-item'})

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('a').text.strip()
        link = sd.find('a')['href'].strip()
        city = sd.find('ul', attrs={'class': 'list-inline list-group-item-text'}).text.strip().split('\n')[0].split(',')[0].strip()

        if city == 'Remote':
            city = ''
            type = 'remote'
        else:
            type = 'on-site'

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "totalsoft",
                "country": "Romania",
                "city": city,
                "remote": type,
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
