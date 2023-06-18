#
#
#
# Scraper for new Company ---> MorningStar
# Company careers link ---> https://www.sustainalytics.com/our-careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
import re


def get_cookie_and_csrfToken() -> dict:
    """
    Get new data for requests: Cookie and Token.
    """

    response = requests.head('https://morningstar.wd5.myworkdayjobs.com/Sustainalytics').headers

    cookie = str(response['Set-Cookie'])

    # regex
    new_dict = dict(wday_vps_cookie=r'wday_vps_cookie=([^;]+)',
                    PLAY_SESSION='PLAY_SESSION=([^;]+)',
                    TS014c1515='TS014c1515=([^;]+)',
                    wd_broser_id='wd-browser-id=([^;]+)',
                    CALYPSO_CSRF_TOKEN='CALYPSO_CSRF_TOKEN=([^;]+)')

    # catch data from requests and store it in new dict
    regex_dict = dict()
    for key, value in new_dict.items():
        match = re.search(value, cookie)
        if match:
            regex_form = match.group(1)
            regex_dict[key] = regex_form

    return regex_dict


def make_post_request() -> tuple:
    """
    ... data for post requests.
    """

    # data for requests to this site
    data = get_cookie_and_csrfToken()

    url = 'https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Sustainalytics/jobs'

    headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': f"wday_vps_cookie{data['wday_vps_cookie']}; PLAY_SESSION={data['PLAY_SESSION']} TS014c1515={data['TS014c1515']}; timezoneOffset=-180; wd-browser-id={data['wd_broser_id']}; CALYPSO_CSRF_TOKEN={data['CALYPSO_CSRF_TOKEN']}",
            'Origin': 'https://morningstar.wd5.myworkdayjobs.com',
            'Referer': 'https://morningstar.wd5.myworkdayjobs.com/Sustainalytics',
            'Referer':'https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics/jobs?locations=0e19b52288b501a1c52ad54eda00f640',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-CALYPSO-CSRF-TOKEN': f"{data['CALYPSO_CSRF_TOKEN']}",
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

    payload = '{"appliedFacets":{},"limit":20,"offset":0,"searchText":""}'

    return url, headers, payload


def collect_data_from_morningstar() -> list:
    """
    ... collect data from morning star. All data with one requests.
    """

    data = make_post_request()
    response = requests.post(
            url=data[0],
            headers=data[1],
            data=data[2])

    lst_with_data = []
    for dt in response.json()['jobPostings']:
        link = dt['externalPath']
        title = dt['title']

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link":  'https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics' + link,
            "company": "sustainalytics",
            "country": "Romania",
            "city": "Romania"
            })

    # print data to terminal
    print(f'Sustainalytics - Numarul total de joburi ---> {len(lst_with_data)}')
    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'sustainalytics'
data_list = collect_data_from_morningstar()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('sustainalytics',
                  'https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Sustainalytics/sidebarimage/e05e932c1513013fd79b39762702c601'
                  ))
