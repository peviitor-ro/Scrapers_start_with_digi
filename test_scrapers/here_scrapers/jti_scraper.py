#
#
#
# Scrape J.T. INTERNATIONAL (ROMANIA) SRL
# Link to data ---> https://jobs.jti.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
from math import ceil
import time


def set_global_headers():
    """
    Set headers for my new site requests.
    """

    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=w2~8DC473DD77A5A2566F96CB04AAA08C02; OptanonConsent=isIABGlobal=false&datestamp=Fri+Apr+28+2023+23%3A35%3A54+GMT%2B0300+(Eastern+European+Summer+Time)&version=6.14.0&hosts=&consentId=6701dcca-95bc-4d6b-a6b6-2387ec1374fd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0003%3A0&AwaitingReconsent=false',
            'Origin': 'https://jobs.jti.com',
            'Referer': 'https://jobs.jti.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-CSRF-Token': '2079eb60-a83a-4f6c-bda9-8b3604238d81',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

    return headers


def return_page_num() -> int:
    """
    This func() return number of all jobs from current website.
    ... func return two numbers 1. nums of jobs, 2 - jobs on one page.
    """

    num_response = requests.get(
            'https://jobs.jti.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=',
            headers=set_global_headers())
    num_soup = BeautifulSoup(num_response.text, 'lxml')

    num_of_jobs = num_soup.find('span', class_='paginationLabel').text.split()
    jobs_num = num_of_jobs[-1]
    jobs_on_one_page = num_of_jobs[-3]

    return int(jobs_num), int(jobs_on_one_page)


def make_requests_get_data(page_num: int):
    """
    This func() make a requests and scrap all data from the site.
    """

    response = requests.get(
            f'https://jobs.jti.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_country=RO&startrow={page_num}',
            headers=set_global_headers()
            )
    soup = BeautifulSoup(response.text, 'lxml')

    soup_span = soup.find_all('span', class_='jobTitle hidden-phone')

    list_with_data = []
    for sp in soup_span:
        link = sp.find('a')['href']
        title = sp.find('a').get_text()

        list_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://jobs.jti.com' + link,
            "company": "jti",
            "country": "Romania",
            "city": "Romania"
        })

    return list_with_data


def run_scraper() -> tuple:
    """
    All data store here. This script extend lst_with data and
    store it in json file.
    """

    lst_with_jobs = []

    # page nums and jobs on one page
    num_jobs, jobs_on_pages = return_page_num()
    iterations = ceil(num_jobs / jobs_on_pages)

    page = 0
    for dt in range(0, iterations):
        data_for = make_requests_get_data(page)

        # extend lst with data
        lst_with_jobs.extend(data_for)

        page += 25
        time.sleep(1)

    return lst_with_jobs, len(lst_with_jobs)
