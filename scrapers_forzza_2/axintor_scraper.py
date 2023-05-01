#
#
#
# New Scraper for PeViitor
# Link to job portal ---> https://www.axintor.be/ro/locuri-de-munca?sector=&jobtitle=&sortorder=asc&searchterm=
#
import requests
from bs4 import BeautifulSoup
#
import uuid
import json
#
import re


def set_global_headers() -> dict:
    """
    Standard headers for request axintor website.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    return headers


def collect_data_from_axintor(url: str) -> list:
    """
    Collect data from Axintor and return a list with json data.
    """

    response = requests.get(url=url, headers=set_global_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a')

    # store all data and remove duplicates
    lst_with_data = []
    for new_sd in soup_data:
        if new_sd.find('h3', class_="listing__title"):
            # catch title
            final_title_1 = new_sd.find('h3', class_='listing__title').text
            final_title_2 = new_sd.find('p', class_='wage').text

            job_final_title = final_title_1 + ' ' + final_title_2

            # link
            match = re.search(r'href="([^"]+)"', str(new_sd))
            if match:
                href = 'https://www.axintor.be' + match.group(1)

                # here append data to list
                gita = (job_final_title, href)

                lst_with_data.append(gita)

    # here make a list with data json!
    lst_with_json = []
    for key, value in dict(lst_with_data).items():

        # save data to list
        lst_with_json.append({
            "id": str(uuid.uuid4()),
            "job_title": key,
            "job_link":  value,
            "company": "axintor",
            "country": "Romania",
            "city": "Romania"
            })

    # return json with jobs
    return lst_with_json


def scrape_axintor() -> None:
    """
    Scrape data from website Axintor and store all data to json.
    """

    all_json_data = collect_data_from_axintor(
            'https://www.axintor.be/ro/locuri-de-munca?sector=&jobtitle=&sortorder=asc&searchterm='
            )

    # save data to josn!
    with open('scrapers_forzza_2/data_axintor.json', 'w') as new_file:
        json.dump(all_json_data, new_file)

    print('Axintor ---> Done!')
