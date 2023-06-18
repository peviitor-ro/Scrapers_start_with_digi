#
#
#
# New scraper for Canam
# Link to this jobs ---> https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def collect_data_from_canam():
    """
    Func() for collect data from CANAM.
    >>> Collect data with Get Requests.
    """

    response = requests.get('https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='c-card-job')

    lst_with_jobs = []
    for sd in soup_data:
        link = sd['href']
        title = sd.find('span').text

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "canam",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'canam'
data_list = collect_data_from_canam()
scrape_and_update_peviitor(company_name, data_list)

# update Logo
print(update_logo('canam', 'https://www.canam.com/wp-content/themes/canam/dist/img/logo-canam.png'))
