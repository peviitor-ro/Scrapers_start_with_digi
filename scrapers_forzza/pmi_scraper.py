#
#
#
# Scraper for pmi.com!
# Link to this domain careers -> https://www.pmi.com/careers/explore-our-job-opportunities?title=&locations=Romania&departments=&contracts=&page=1
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#
import time
from random import randint


def set_headers():
    """
    Set headers for request to pmi.com!
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return HEADERS


def get_data_from_pmi(url: str):
    """
    This func() sent requests direct to url. Wait html response.
    """

    response = requests.get(url=url, headers=set_headers())
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

    # save data to json!
    with open('scrapers_forzza/data_pmi.json', 'w') as new_file:
        json.dump(all_job_data_from_pmi, new_file)

    print("... pmi ---> Done!")
