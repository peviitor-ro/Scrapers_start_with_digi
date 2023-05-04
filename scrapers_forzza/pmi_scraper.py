#
#
#
# Scraper for pmi.com!
# Link to this domain careers -> https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#


def get_data_from_pmi(url: str):
    """
    This func() sent requests direct to url. Wait html response.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # get all needed data from html
    soup_data = soup.find_all('a', class_='job-row')

    # list with data from 1 page
    list_with_data_pmi = []
    for si in soup_data:
        link = si['href'].strip()
        title = si.find('h3').text.strip()

        list_with_data_pmi.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  'https://www.pmi.com' + link,
                "company": "pmi",
                "country": "Romania",
                "city": "Romania"
            })

    return list_with_data_pmi, soup


def scrape_pmi():
    """
    This func() is about scrape pmi. General function.
    """

    all_job_data_from_pmi = []

    count_it = 1
    # get data!
    while True:
        job_data = get_data_from_pmi(
                f'https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page={count_it}'
            )
        all_job_data_from_pmi.extend(job_data[0])

        # check if next link is valid
        try:
            try_link_next = job_data[1].find('a', class_='pages-nav--last')['href']
        except:
            try_link_next = '-'

        if try_link_next != '-' and try_link_next != None:
            count_it += 1
            continue
        else:
            break

    return all_job_data_from_pmi


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'pmi'
data_list = scrape_pmi()
scrape_and_update_peviitor(company_name, data_list)
