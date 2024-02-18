#
#
# Config for Dynamic Post Method -> For Json format!
#
# Company ---> FlowxAI
# Link ------> https://apply.workable.com/flowxai/
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
    PostRequestJson,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,

    # for this time
    GetHeadersDict,

    get_data_with_regex,
)

def get_cookie_ids():
    '''
        ... get unic ids for cookie, headers
    '''
    string_regex_data = str(GetHeadersDict('https://apply.workable.com/flowxai/'))

    return get_data_with_regex('__cf_bm=([^;]+);', string_regex_data), get_data_with_regex('wmc=([^;]+);', string_regex_data)


def prepare_headers():
    '''
        ... prepare post personalized post requests
    '''
    data_ids = get_cookie_ids()
    #
    url = 'https://apply.workable.com/api/v3/accounts/flowxai/jobs'
    headers = {
        'authority': 'apply.workable.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'content-type': 'application/json',
        'cookie': f'{data_ids[1]} {data_ids[0]} _dd_s=rum=0&expire=1708242969216',
        'origin': 'https://apply.workable.com',
        'referer': 'https://apply.workable.com/flowxai/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    payload =  '{"query":"","location":[{"country":"Romania","region":"Bucharest","city":"Bucharest","countryCode":"RO"}],"department":[],"worktype":[],"remote":[],"workplace":[]}' 

    return url, headers, payload


def scraper():
    '''
    ... scrape data from FlowxAI scraper.
    '''

    data_prepare_headers = prepare_headers()
    #
    post_data = PostRequestJson(url=data_prepare_headers[0], custom_headers=data_prepare_headers[1], data_raw=data_prepare_headers[2])

    job_list = []
    for job in post_data.get('results'):
        
        if (location := job.get('location').get('city').lower()) == 'bucharest':
            location = 'Bucuresti'

        # get jobs items from response
        job_list.append(Item(
            job_title=job.get('title'),
            job_link=f'https://apply.workable.com/flowxai/j/{job.get("shortcode")}/',
            company='FlowxAI',
            country='Romania',
            county=get_county(location),
            city=location,
            remote=job.get('workplace'),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "FlowxAI"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)

if __name__ == '__main__':
    main()
