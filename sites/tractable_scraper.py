#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Tractable
# Link ------> https://tractable.ai/en/jobs
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
    #
    GetHeadersDict,
)


def get_etag_W_slash():
    '''
    This function return the code: W/ for 304 redirect.

    params: None
    return: etag: str
    '''

    return GetHeadersDict('https://tractable.ai/en/jobs').get('Etag')


def make_headers():
    '''
    This function is about Headers for Tractable.ai's API.

    params: None
    returns: url: str, headers: dict
    '''

    url = 'https://tractable.ai/api/joblist?board=tractable'
    
    headers = {
        'authority': 'tractable.ai',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'if-none-match': f'{get_etag_W_slash()}',
        'referer': 'https://tractable.ai/en/jobs',
        'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    return url, headers


def scraper():
    '''
    ... scrape data from Tractable scraper.
    '''

    url, headers = make_headers()

    json_data = GetRequestJson(url=url, custom_headers=headers)
    print(json_data)

    job_list = []
    # for job in json_data['key']:
    #     pass

    #     # get jobs items from response
    #     job_list.append(Item(
    #         job_title='',
    #         job_link='',
    #         company='Tractable',
    #         country='',
    #         county='',
    #         city='',
    #         remote='',
    #     ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Tractable"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
