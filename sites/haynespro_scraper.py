#
#
#
# Scraper for HaynesPro Company
# Link to company career page -> https://www.haynespro.com/careers
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

def collect_data_from_haynespro() -> list[dict]:
    '''
    ... this function collects all data and returns a list with jobs
    '''

    response = requests.get(url='https://www.haynespro.com/careers', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('span', class_='field-content')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('h3').find('a').text
        link = 'https://www.haynespro.com' + sd.find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "HaynesPro",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'HaynesPro'
data_list = collect_data_from_haynespro()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('HaynesPro',
                  "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/032019/untitled-1_149.png?u.8VuLl0JL541X9uIuiXD0XH8kZ3_lt.&itok=hu0Z7YHB"
                  ))
