#
#
#
# Scraper for OSF Digital Company
# Link to ---> https://osf.digital/careers/jobs?location=romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import re


# this is instance for session. Scraper need this because
# ... it use fresh cookie evrey time
session = requests.Session()


def get_ids() -> tuple:
    '''
    ... return fresh cookie data from OSF.
    '''

    res = session.head(url='https://osf.digital/careers/jobs?location=romania',
                       headers=DEFAULT_HEADERS).headers

    # search cookie by regex
    return re.search(r"__RequestVerificationToken=([A-Za-z0-9_-]+);", str(res)).group(0)


def set_headers() -> tuple:
    """
    Set default headers for scraping.
    """
    token_cookie = get_ids()

    url = 'https://osf.digital/careers/jobs?location=romania'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '\'' + token_cookie + ' CookieConsent={stamp:%27gF2wOFqMFWAwPXKKsC7/bA566Qm6ilqaFpgbB03SHW1hzoOyQCLpqA==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1691269536897%2Cregion:%27ro%27}',
        'Origin': 'https://osf.digital',
        'Referer': 'https://osf.digital/careers/jobs?location=romania',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        }

    data = {
        'scController': 'OsfCommerceJob',
        'scAction': 'GetItems',
        'parameter': 'request',
        '__RequestVerificationToken': f'{token_cookie.split("=")[1][:-1]}'
        }

    return url, headers, data


def collect_data_osf() -> list:
    """
    Collect all data with session. OSF!
    """
    data = set_headers()
    response = session.post(
            url=data[0],
            headers=data[1],
            data=data[2]
            )
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='section-positions section-border')

    list_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='blue-link')['href']
        title = sd.find('h4').text

        list_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": "https://osf.digital" + link,
                "company": "osf",
                "country": "Romania",
                "city": "Romania"
            })

    return list_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'osf'
data_list = collect_data_osf()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('osf',
                  'https://osf.digital/library/media/osf/digital/common/header/osf_digital_logo.svg?h=60&la=en&w=366&hash=5FF21BA406E10D94D9778FA8A3A8AEC43C247D2B'))
