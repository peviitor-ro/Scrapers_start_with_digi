#
#
#
# New Scraper for Suvoda Company
# Link to this Company ---> https://boards.greenhouse.io/embed/job_board?for=suvoda&b=https%3A%2F%2Fwww.suvoda.com%2Fcareers%2Fjob-openings
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def special_headers():
    """
    Define special headers for requests.
    """

    headers = {
        'authority': 'www.suvoda.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfruid=270f54863cc6f05f871b72548d9bd41f223194dc-1683471130; __cf_bm=oRBuLiQx10YKu56b1eX3u6CqxfpCMyHRJ2erjv6uds4-1683473698-0-AcDhd2Ey24p6vd5U9398ovnvbOCkOffYQt9JwoLtK0lo59rrAXD+uOidgcfMce+zbI5AHRlTQwsfKVolrt4Blic=',
        'referer': 'https://www.suvoda.com/careers/job-openings',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
      }

    return headers


def collect_data_from_suvoda():
    """
    Collect data with Get Requests from Suvoda.
    """

    response = requests.get('https://boards.greenhouse.io/embed/job_board?for=suvoda&b=https%3A%2F%2Fwww.suvoda.com%2Fcareers%2Fjob-openings',
                            headers=special_headers())
    soup = BeautifulSoup(response.content, 'lxml')

    lst_with_data = []
    for dt in soup.find_all('div', class_='opening'):
        if 'Romania' in str(dt.find('span', class_='location')):
            link = dt.find('a')['href']
            title = dt.find('a').text

            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link":  link,
                "company": "suvoda",
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


company_name = 'suvoda'
data_list = collect_data_from_suvoda()
scrape_and_update_peviitor(company_name, data_list)
