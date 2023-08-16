#
#
#
# New Scraper For ---> agilefreaks
# Link to this Company ---> https://careers.agilefreaks.com/jobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_site():
    """
    Collect data from https://careers.agilefreaks.com/jobs
    """

    response = requests.get('https://careers.agilefreaks.com/jobs', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='w-full')

    lst_wit_data = []
    for sd in soup_data:
        link = sd.find('a')['href'].strip()
        title = sd.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style').text

        lst_wit_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "AgileFreaks",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_wit_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'AgileFreaks'
data_list = collect_data_from_site()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AgileFreaks',
                  'https://www.agilefreaks.com/sites/default/files/agile-freaks-logo%20%281%29%20%281%29.png'
                  ))
