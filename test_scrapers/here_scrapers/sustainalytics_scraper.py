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


def make_post_request() -> tuple:
    """
    ... data for post requests.
    """
    url = 'https://morningstar.wd5.myworkdayjobs.com/wday/cxs/morningstar/Sustainalytics/jobs'

    headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'PLAY_SESSION=757c64e983e1c932f509c553206ce2d95923d851-morningstar_pSessionId=nj5mvehdpknrcmvc3s2bpsited&instance=wd5prvps0004h; wday_vps_cookie=2938515978.6195.0000; timezoneOffset=-180; TS014c1515=018b6354fee20d4e77b4e9eecc8b3a757d95f412d360c4527c7276a83e9f232e03c160134c6d8bf920c3e62b34a9d6440902e4d826; wd-browser-id=1c1030b1-db9f-4c80-b186-1bbe94033d44; CALYPSO_CSRF_TOKEN=4bd3af53-32c0-4379-97b5-79a18144fe4b',
            'Origin': 'https://morningstar.wd5.myworkdayjobs.com',
            'Referer': 'https://morningstar.wd5.myworkdayjobs.com/en-US/Sustainalytics/jobs?locations=0e19b52288b501a1c52ad54eda00f640',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-CALYPSO-CSRF-TOKEN': '4bd3af53-32c0-4379-97b5-79a18144fe4b',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

    payload = '{"appliedFacets": {"locations": ["0e19b52288b501a1c52ad54eda00f640","0e19b52288b5019ff735e44eda00fe40"]}, "limit": 20, "offset": 0, "searchText": ""}'

    return url, headers, payload


def run_scraper() -> tuple:
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

    return lst_with_data, len(lst_with_data)
