#
#
#
# Scrape new Site -> ThreatConnect
# Link to this site -> https://jobs.lever.co/threatconnect?_ga=2.19358907.2008016264.1682672901-1880994929.1682672901
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json


def set_headers():
    """
    Set headers for this new site. This site return only html.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def return_list_with_jobs(url: str):
    """
    Return html data from ThreatConnect.
    """

    response = requests.get(url=url, headers=set_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='posting')

    lst_with_jobs = []
    for sd in soup_data:
        link = sd.find('a', class_='posting-title')['href']
        title = sd.find('h5').text.strip()

        lst_with_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "threatconnect",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_jobs


def threatconnect_scrape():
    """
    Scrape finall func(). General func().
    """

    lst_with_data = return_list_with_jobs('https://jobs.lever.co/threatconnect?_ga=2.19358907.2008016264.1682672901-1880994929.1682672901')

    # save data to json
    with open('scrapers_forzza/data_threatconnect.json', 'w') as new_file:
        json.dump(lst_with_data, new_file)

    print('ThreatConnect ---> Done!')
