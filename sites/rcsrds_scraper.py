#
#
#
# Scraper for digi.ro ---> Cariere.
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import re
import uuid
#
import time


def get_cookie() -> str:
    '''
    ... here is the function for getting cookies.
    '''
    return requests.head('https://www.digi.ro/cariere').headers['Set-Cookie'].split(';')[0]


# headers for post requests
def get_post_data(city: str, job_title: str) -> tuple:
    """
    This funct() is about special headers for CITIES and JOB_TITLE.
    """

    url = 'https://www.digi.ro/cariere/search-xhr'

    headers = {
            'authority': 'www.digi.ro',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'{get_cookie()}; webpush=0; cmp_level=15',
            'origin': 'https://www.digi.ro',
            'referer': 'https://www.digi.ro/cariere',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    data = {
        'action': 'assistanceSupportCareers',
        'company': 'rcs-rds',
        'county':  city,
        'industry': job_title
    }

    return url, headers, data


def get_cities_and_jobs_name(url: str, session) -> tuple:
    """
    This func() parse html and return list with cities name and jobs name.
    """

    local_headers = {
        "User-Agent": "ltx71 - (http://ltx71.com/)",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
        }

    response = session.get(url=url, headers=local_headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # get cities names
    cities = soup.find('select', {'name': 'form-assistance-support-careers-county'})
    jobs = soup.find('select', {'name': 'form-assistance-support-careers-industry'})

    patern = re.compile('value="([^"]*)"')
    cities_lst = patern.findall(str(cities))[1:]
    jobs_lst = patern.findall(str(jobs))[1:]

    return cities_lst, jobs_lst


def scrape_data_from_digi(cities: list, jobs: list, session) -> list:
    """
    This func() is about scrape data from digi-rds.
    """

    lst_with_jobs = []
    for city in cities:
        for job in jobs:

            # start scrape data
            returned_head = get_post_data(city=city, job_title=job)
            response = session.post(url=returned_head[0], headers=returned_head[1], data=returned_head[2])

            soup = BeautifulSoup(response.text, 'lxml')

            job_titles = re.findall(r'<label class="accordion-title"[^>]*>([^<]+)<', str(soup))
            job_links = re.findall(r'href="([^"]+)"', str(soup))

            # print(job_links, job_titles)

            # print data to see how it work
            print(f"{city} - {job}")

            # data from post requests in list
            # job_titles = [tag.text for tag in soup.find_all('label', class_='accordion-title')]
            # job_links = [links['href'] for links in soup.find_all('a', class_='btn-round-right')]

            if (len(job_titles) == len(job_links)) and (len(job_titles) + len(job_links)) > 0:
                for id in range(len(job_titles)):

                    time.sleep(0.3)

                    # append data to list
                    lst_with_jobs.append({
                            "id": str(uuid.uuid4()),
                            "job_title": job_titles[id],
                            "job_link":  'https://digi.ro/' + str(job_links[id]),
                            "company": "rcsrds",
                            "country": "Romania",
                            "city": city
                            })

    return lst_with_jobs


def rcsrds_scrape():

    session = requests.Session()

    tuple_jobs_cities = get_cities_and_jobs_name(url='https://www.digi.ro/cariere', session=session)
    print(tuple_jobs_cities)

    lst_with_data_post = scrape_data_from_digi(cities=tuple_jobs_cities[0], jobs=tuple_jobs_cities[1], session=session)

    return lst_with_data_post


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'rcsrds'
data_list = rcsrds_scrape()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('rcsrds',
                  'https://www.digi.ro/static/theme-ui-frontend/bin/images/logo-digi-alt.png'
                  ))
