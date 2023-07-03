# Scraper for Sostenia Company
# Link to company career page -> https://www.sostenia.ro/en/jobs
#
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid

def collect_data_from_sostenia():
    '''
    ... this function will collect all data and will return a list with jobs
    '''

    response = requests.get(url='https://www.sostenia.ro/en/jobs', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='col-lg')
    # print(soup_data)

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h3').find('span').text
        link = "https://www.sostenia.ro" + sd.find('a')['href']
        # print(title,link)

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Sostenia",
            "country": "Romania",
            "city": "Romania"
        })
    return lst_with_data,len(lst_with_data)


print(collect_data_from_sostenia())
