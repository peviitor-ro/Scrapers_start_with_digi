#
#
#
# Company -> cegedim
# Link to -> https://careers.cegedim.com/en/annonces
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def prepare_post_data() -> tuple:
    '''
    ... prepare data for post requests with python.
    url, headers, data.
    '''

    url = 'https://api.digitalrecruiters.com/public/v1/careers-site/job-ads?domainName=careers.cegedim.com&limit=20&page=1&locale=en_GB'

    headers = {
            'authority': 'api.digitalrecruiters.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://careers.cegedim.com',
            'referer': 'https://careers.cegedim.com/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36' 
        }

    data = {
            "filters": {},
            "viewport": {
                "top_left": {
                    "lat": 51.46896241876855,
                    "lon": 18.552639878467087
                },
                "bottom_right": {
                    "lat": 25.979625107607177,
                    "lon": 38.72353831596708
                }
            }
        }

    return url, headers, data


def make_post_requests() -> list:
    '''
    ... make post requests and return all data in json file,
    after in a list file to store it in a list and send it
    to peviitor.ro.
    '''

    data = prepare_post_data()
    response = requests.post(url=data[0], headers=data[1], json=data[2]).json()

    lst_with_data = []
    for dt in response['items']:
        link = 'https://careers.cegedim.com/en/annonce/' + dt['url']
        title = dt['title']
        city = dt['location']

        lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "cegedim",
                "country": "Romania",
                "city": city
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'cegedim'
data_list = make_post_requests()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('cegedim',
                  'https://careers.cegedim.com/generated_contents/images/company_logo_career/LRzK3bVZ-cegedim-logo2010-detoure200x73.png'))
