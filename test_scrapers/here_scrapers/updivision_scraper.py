#
#
#
# Company -> updivision
# Link -> https://updivision.com/careers?variable=tech
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def run_scraper() -> tuple:
    """
    ... return data from site with one requests.
    Request to html.
    """

    response = requests.get(url='https://updivision.com/careers?variable=tech',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='container-jobs')

    lst_with_data = []
    for dt in soup_data:
        title = dt.find('a').text

        # makek url from title
        link = title.lower().replace('.', '').replace('+ ', '').replace('(', '').replace(')', '').replace('& ', '')

        # append all data to list
        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://updivision.com/careers/' + '-'.join(list(link.split())),
                "company": "updivision",
                "country": "Romania",
                "city": "Romania"
            })

    return lst_with_data, len(lst_with_data)
