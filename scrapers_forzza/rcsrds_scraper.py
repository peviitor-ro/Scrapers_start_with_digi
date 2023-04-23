#
#
#
# Scraper for digi.ro ---> Cariere.
#
import requests
from bs4 import BeautifulSoup
import re
import json
import uuid
from random import randint
import time


# start count time
start_time = time.time()


def split_special_name(name: str) -> str:
    """ func() to convert to normal string for requests.
    """
    print(f" Jobul {name} ---> scrapuit.")
    if ',' in name:
        name = name.replace(',', '%2C')
        new_name = "+".join(name.split())
        return new_name.strip()

    elif name and len(name.split()) > 1:
        new_name_2 = "+".join(name.split())
        return new_name_2.strip()

    else:
        return name


# headers for post requests
def get_post_data(city: str, job_title: str) -> tuple:
    """
    This funct() is about special headers for CITIES and JOB_TITLE.
    """

    url = 'https://www.digi.ro/cariere/search-xhr'

    headers = {
        'authority': 'www.digi.ro',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'DGROSESSV3PRI=BAF20A5FBB184D59BDF54256B7C5B2EE8F75B2552801437C; webpush=0; cmp_level=15',
        'origin': 'https://www.digi.ro',
        'referer': 'https://www.digi.ro/cariere',
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

    data = {
        'action': 'assistanceSupportCareers',
        'company': 'rcs-rds',
        'county':  city,
        'industry': split_special_name(job_title)
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

            soup = BeautifulSoup(response.content, 'lxml')

            # data from post requests in list
            job_titles = [tag.text for tag in soup.find_all(attrs={"class": "accordion-title"})]
            job_links = [links.a['href'] for links in soup.find_all(attrs={"class": "align-right"})]

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

                    print(f"Jobul {job} ---> a fost scrapuit")
            print(f"Scraping on job ---> in {city}")
            time.sleep(randint(1, 2))
        print("=================================")

    # sorted results
    new_lst = []
    for diction in lst_with_jobs:
        new_lst.append(diction['job_link'])

    returned_list = []
    unic_links = list(set(new_lst))
    for unic_link in unic_links:
        for data_dict in lst_with_jobs:
            if unic_link == data_dict['job_link']:
                returned_list.append(data_dict)

                break

    print(len(returned_list))

    return returned_list


def rcsrds_scrape():

    session = requests.Session()

    tuple_jobs_cities = get_cities_and_jobs_name(url='https://www.digi.ro/cariere', session=session)
    print(tuple_jobs_cities)

    lst_with_data_post = scrape_data_from_digi(cities=tuple_jobs_cities[0], jobs=tuple_jobs_cities[1], session=session)

    with open('scrapers_forzza/data_digi.json', 'w') as file:
        json.dump(lst_with_data_post, file)

    finish_time = time.time() - start_time
    print(f"Script execute in {int(finish_time) / 60}")
