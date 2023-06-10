#
#
#
# New Scraper for PeViitor
# Link to job portal ---> https://www.axintor.be/ro/locuri-de-munca?sector=&jobtitle=&sortorder=asc&searchterm=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
#
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import re


# collect data from axintor
def run_scraper(url='https://www.axintor.be/ro/locuri-de-munca?sector=&jobtitle=&sortorder=asc&searchterm=') -> tuple:
    """
    Collect data from Axintor and return a list with json data.
    """

    response = requests.get(url=url, headers=DEFAULT_HEADERS)
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
    return lst_with_json, len(lst_with_data)
