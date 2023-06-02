#
#
#
# Scraper for Bitpanda Company
# link to compapy -> https://www.bitpanda.com/en/career
# link to API -> https://boards.eu.greenhouse.io/bitpanda
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_API():
    """
    ... this func() collect all data and return a list with json() data.
    """

    response = requests.get('https://boards.eu.greenhouse.io/bitpanda',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='opening')

    lst_with_data = []
    for dt in soup_data:

        # check if Romania in location
        location = dt.find('span', class_='location').text
        if 'Romania' in location or 'România' in location:
            title = dt.find('a').text
            link = dt.find('a')['href']

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://boards.eu.greenhouse.io/' + link,
                    "company": "bitpanda",
                    "country": "Romania",
                    "city": location.split(', ')[0]
                })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'bitpanda'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('bitpanda',
                  'https://cdn.bitpanda.com/media/New%20navigation_Rebrand%203.0/Bitpanda_EN_trimmed.png'
                  ))
