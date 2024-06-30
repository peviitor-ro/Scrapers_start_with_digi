#
#
# Your custom scraper here ---> Last level!
#
# Company ---> Skywind
# Link ------> https://skywindgroup.bamboohr.com/careers/list
#
#
# Aici va invit sa va creati propriile metode de scraping cu Python,
# ... folosind:
# -> requests
# -> BeautifulSoup
# -> requests_html etc.
#
from __utils import(
    Item,
    get_county,

    UpdateAPI,
    GetHeadersDict,
)
import requests


def get_cookie_keys():
    '''
    ... this function get dynamic keys for request to API endpoint.

    params: None
    return: tuple with keys -> 
        PHPSESSID
        _cfuvid
    '''

    cookie_data_list = GetHeadersDict('https://skywindgroup.bamboohr.com/careers/').get('Set-Cookie').split()
    #
    phpsessionID = ''
    cf__token = ''

    # get secret keys for site
    for secret_data in cookie_data_list:
        if 'PHPSESSID' in secret_data:
            phpsessionID = secret_data
        elif 'cfuvid' in secret_data:
            cf__token = secret_data

    return phpsessionID, cf__token


def make_headers():
    '''
    ... function for making headers for GetRequest
    params: None
    return: tuple with url, cookie data and headers.
    '''

    # return dynamic keys in function
    phpsession, cf__token = (get_cookie_keys())

    url = 'https://skywindgroup.bamboohr.com/careers/list'

    cookies = {
        'PHPSESSID': phpsession,
        '_cfuvid': cf__token,
    }

    headers = {
        'authority': 'skywindgroup.bamboohr.com',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://skywindgroup.bamboohr.com/careers/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, cookies, headers


def scraper():
    '''
    ... scrape data from Skywind scraper.
    Your solution!
    '''

    url, cookies, headers = make_headers()
    response = requests.get(url=url, cookies=cookies, headers=headers).json()

    job_list = []
    for job in response.get('result'):

        # get Romanian counties names
        county_ro = job.get('location').get('state')
        if county_ro:
            if county_ro.lower() == 'bucharest':
                county_ro = 'Bucuresti'

        # get Romanian cities names
        city_ro = job.get('location').get('city')
        if city_ro:
            city_ro = city_ro.split(',')[0].lower()
            if city_ro.lower() == 'bucharest':
                city_ro = 'Bucuresti'

        # remote
        is_remote = job.get('isRemote')

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('jobOpeningName'),
            job_link=f"https://skywindgroup.bamboohr.com/careers/{job.get('id')}",
            company='Skywind',
            country='Romania',
            county=county_ro.title() if county_ro is not None else None,
            city=city_ro.title() if city_ro is not None else None,
            remote='on-site' if is_remote == None else is_remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Skywind"
    logo_link = "https://www.gamblerspick.com/uploads/monthly_2018_08/swg.png.394346b9cd7ee1cb87d519437228f8e2.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
