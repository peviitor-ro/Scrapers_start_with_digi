#
#
#
# New scraper for IMC
# Link to this -> 
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def post_headers() -> tuple:
    """
    Post headers for new post requests.
    """
    url = 'https://www.im-c.com/wp-admin/admin-ajax.php'

    headers = {
            'authority': 'www.im-c.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'CookieConsent={stamp:%27fG18s+xDdiaXLD/RAEP/atIjbk9vd+9PX7E2rH/aQvCoYaSjFrosmA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1684081288570%2Cregion:%27ro%27}',
            'origin': 'https://www.im-c.com',
            'referer': 'https://www.im-c.com/careers/job-offers/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

    params = {'action': 'get_other_list_items', 'posttype': 'post_type_job', 'ppp': '50', 'paged': '1', 'filters': 'taxonomy_of_location_jobs:sibiu'}

    return url, headers, params


def collect_data_from_imc() -> list:
    """
    ... collect data from imc.
    """

    res = post_headers()
    response = requests.post(url=res[0], headers=res[1], data=res[2])
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='result result--post_type_job')

    lst_with_data = []
    for sd in soup_data:
        title = sd.find('div', class_='result__title').text
        link = sd.find('div', class_='result__cta').find('a')['href']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  link,
            "company": "imc",
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


company_name = 'imc'
data_list = collect_data_from_imc()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('imc',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgMERA2UEWcjsDuh1YsmPozwdgUlRNOP5xev4jwtSt&s'
                  ))
