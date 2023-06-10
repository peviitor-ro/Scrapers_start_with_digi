#
#
#
# Scraper for OSF Digital Company
# Link to ---> https://osf.digital/careers/jobs?location=romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def set_headers() -> tuple:
    """
    Set default headers for scraping.
    """

    url = 'https://osf.digital/careers/jobs?location=romania'

    headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
             'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '__RequestVerificationToken=kpTO_9WZW3pOy75NA-0BR6W7mqJpyqlfoK8W-1VPCGo4gASGHh2Z_Knp31rwbf0BgE3TM-xDcTuaMn6T7YfWqLNAyt41; ASP.NET_SessionId=dwkpwrwqwhxqpnhisacucsr2; CookieConsent={stamp:%27x7uXJqRZohYFzf3eRobuXgRXFC9Mqs0zpkQIUIMidEc+uzuQysCDvw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1684179516211%2Cregion:%27ro%27}; SC_ANALYTICS_GLOBAL_COOKIE=33fa9e79dfbb416699b3b7d558be6305|True',
            'Origin': 'https://osf.digital',
            'Referer': 'https://osf.digital/careers/jobs?location=romania',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

    query_params = {
            "scController": "OsfCommerceJob",
            "scAction": "GetItems",
            "parameter": "request",
            "__RequestVerificationToken": "NyvePAz4BlExbdD3T6Cy_unJv67n9mfU003xcPtjajGVf5lOKsGBJrXRvIjbFdWZnBsH7IfIsj6Y-8vLecm3_EyiTZ81"
        }

    return url, headers, query_params


def run_scraper() -> tuple:
    """
    Collect all data with session. OSF!
    """
    data = set_headers()
    response = requests.post(
            url=data[0],
            headers=data[1],
            data=data[2]
            )
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='section-positions section-border')

    list_with_data = []
    for sd in soup_data:
        link = sd.find('a', class_='blue-link')['href']
        title = sd.find('h4').text

        list_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": "https://osf.digital" + link,
                "company": "osf",
                "country": "Romania",
                "city": "Romania"
            })

    return list_with_data, len(list_with_data)
