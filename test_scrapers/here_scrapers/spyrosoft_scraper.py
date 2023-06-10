#
#
#
# New scraper for spyro-soft!
# Link for this scraper ---> https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
from random import randint


def set_post_headers(num_page: int) -> dict:
    """
    Set post_headers for Spyrosoft site.
    """

    url = 'https://spyro-soft.com/wp-admin/admin-ajax.php'

    headers = {
            'authority': 'spyro-soft.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'pll_language=en; _fbp=fb.1.1683561480604.2498753402',
            'origin': 'https://spyro-soft.com',
            'referer': 'https://spyro-soft.com/career?area=all&skills=all&location=romania&experience=all',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    payload = {
        "action": "career_listing",
        "location[]": "romania",
        "search": "",
        "paged": f'{num_page}'
        }

    return url, headers, payload


def collect_data_from_spyrosoft(num: int) -> list:
    """
    Scrape data from Spyrosoft.
    """

    data_post = set_post_headers(num)
    response = requests.post(url=data_post[0], headers=data_post[1], data=data_post[2])
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-sm-6 col-lg-4 CareerThumbnail-col')

    lst_with_data = []
    for sd in soup_data:
        link = sd.find('a')['href'].strip()
        title = sd.find('p', class_='CareerThumbnail__title').text.strip()

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "spyrosoft",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_data


def run_scraper() -> tuple:
    """
    Scrape all data from Spyro.
    """

    page = 1
    flag = True

    lst_with_jobs = []
    while flag != False:

        data_jobs = collect_data_from_spyrosoft(page)

        if len(data_jobs) > 0:
            lst_with_jobs.extend(data_jobs)
            print(f'Scrape on page {page}')
        else:
            flag = False
            print('Scraper do all job!')

        page += 1
        time.sleep(randint(1, 2))


    return lst_with_jobs, len(lst_with_jobs)
