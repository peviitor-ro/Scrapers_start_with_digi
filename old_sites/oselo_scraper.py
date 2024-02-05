#
#
#
#
# Company -> oselo!
# Link ----> https://www.oselorecruitment.com/job-search
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def get_cookie() -> str:
    '''
    ... get cookie from this site.
    '''
    return requests.head(url='https://www.oselorecruitment.com/job-search',
                             headers=DEFAULT_HEADERS).headers['Set-Cookie'].split(';')[0]


def prepare_post_requests() -> tuple:
    '''
    ... here prepare post requests.
    '''

    url = 'https://www.oselorecruitment.com/index.php?option=com_recmgr&view=search&tmpl=component&layout=results'

    headers = {
            'authority': 'www.oselorecruitment.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'{get_cookie()}; oselo_tpl=oselo; resolution=1920; rm-cookies-consent=%7B%22103%22%3A%221%22%2C%22104%22%3A%221%22%7D; MCPopupClosed=yes',
            'origin': 'https://www.oselorecruitment.com',
            'referer': 'https://www.oselorecruitment.com/job-search',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    data = 'keyword=&area=139&type=&sector=&cid='

    return url, headers, data


def get_data_from_oselo():
    '''
    ... get all data from this site and store it into a list with dict.
    '''

    url, headers, data = prepare_post_requests()
    #
    post_response = requests.post(url=url, headers=headers, data=data).json()['main']
    soup = BeautifulSoup(post_response, 'lxml')

    list_with_data = []
    for job in soup.find_all(id='searchedjob'):
        link = 'https://www.oselorecruitment.com' + job.find('a')['href'].strip()
        title = job.find('a').text.strip()

        list_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "oselo",
            "country": "Romania",
            "city": "Remote"
            })

    return list_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'oselo'
data_list = get_data_from_oselo()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('oselo',
                  'https://www.oselorecruitment.com/images/logo.png'
                  ))
