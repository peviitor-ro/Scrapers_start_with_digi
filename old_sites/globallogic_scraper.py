#
#
#
# New company to scrape ---> Globallogic
# Link to this company ---> https://www.globallogic.com/ro/careers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid
#
import time
from random import randint


def prepare_fresh_headers() -> dict:
    '''
    New headers for this site.
    '''
    headers = {
            'authority': 'www.globallogic.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'visid_incap_1279438=NstEv6+BRRu7FbvhJ2CcZqjwZGQAAAAAQUIPAAAAAAAmJ0760cIoQSbzJ7IXZCfb; CookieConsent={stamp:%27Rm4fk9DeBCocbMY0P1wAkhbWQwf/ZwpnE42dfSJEeEb1ig7OJsnysA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1684336814039%2Cregion:%27ro%27}; _mkto_referrer=https://www.globallogic.com/; wordpress_google_apps_login=723fe815ac45b9f516b6603e1ee51d8c; PHPSESSID=nvh3pnotfpbi8l7rjnen7h07u6; locations=romania; incap_ses_1517_1279438=RRK4L/OHbzY7hlXU8XcNFR3EiGQAAAAAMn2VGe+bPbnLR2/z2n6z1g==; incap_ses_1083_1279438=k3IBdee/+0Cpbj+fN5gHD3nFiGQAAAAAkHXIFa8imq/DEcZRxXfClg==; _mkto_datetime=1686685191660',
            'referer': 'https://www.globallogic.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    return headers


def get_soup_object(url: str):
    """
    Get soup object for scraping.
    """

    response = requests.get(url=url,
                            headers=prepare_fresh_headers())

    return BeautifulSoup(response.text, 'lxml')


def get_jobs_num(url: str) -> int:
    """
    Get jobs num from this site.
    ... logic is -> site have something tricky method to scrap.
    I will scrap num jobs, and page after page I will increment
    ... the number of jobs.
    While count_jobs != get_jobs_num... atunci next.
    """

    soup = get_soup_object(url=url)

    numero = soup.find('div', class_='filter-main').find('h5').text.split()[0]

    return int(numero)


def collect_data_from_globalLogic() -> list:
    """
    Here, we scrap all data from ---> GlobalLogic.
    """

    # jobs num from site
    num_jobs = get_jobs_num('https://www.globallogic.com/ro/career-search-page/?keywords=&experience=&locations=romania&c=')
    print(num_jobs)

    page = 1
    jobs_count = 0

    # StopIteration
    stop_page = int(num_jobs / 10) + 1

    lst_with_data = []
    while page <= stop_page:

        soup = get_soup_object("https://www.globallogic.com/ro/career-search-page/?keywords=&experience=&locations=romania&c=")

        # get data from site
        soup_data = soup.find_all('div', class_='career-pagelink')

        # get all data!
        for sd in soup_data:
            link = sd.find('p', class_='mb-0').find('a')['href']
            title = sd.find('p', class_='mb-0').find('a').text

            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  link,
                    "company": "globallogic",
                    "country": "Romania",
                    "city": "Romania"
                    })

            # increment jobs
            jobs_count += 1

            # check jobs count!
            if jobs_count == num_jobs:
                break

        # increment page, go in depth
        print(page)
        page += 1

        # sleep time between requests
        time.sleep(randint(1, 3))

    print(len(lst_with_data))
    print(lst_with_data)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'globallogic'
data_list = collect_data_from_globalLogic()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('globallogic',
                  'https://www.globallogic.com/wp-content/uploads/2021/07/Logo_GL-Hitachi_White-web.svg'
                  ))
