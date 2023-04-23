#
#
#
# Scrape data from wirtek.com/compile
#
import requests
from bs4 import BeautifulSoup
import uuid
#
import json


def set_headers():
    """
    This func() is about create headers for requests.
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def data_scrape_from_wirtek():
    """
    This func() is about scrape wirtek.
    """

    response = requests.get('https://www.wirtek.com/careers', headers=set_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    job_grid = soup.find_all('div', class_='careers-grid__job')

    lst_with_jobs_data = []
    for job in job_grid:
        link_job = job.a['href']
        title_job = job.find('div', class_='careers-grid__job-name').text.strip()

        lst_with_jobs_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title_job,
            "job_link":  link_job,
            "company": "wirtek",
            "country": "Romania",
            "city": "Romania"
            })

    return lst_with_jobs_data


def wirtek_scrape():
    """
    This func() is about logic of all code.
    """

    lst_with_scraped_jobs = data_scrape_from_wirtek()

    # save data to json
    with open('scrapers_forzza/data_wirtek.json', 'w') as file_data:
        json.dump(lst_with_scraped_jobs, file_data)
