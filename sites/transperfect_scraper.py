#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> TransPerfect
# Link ------> https://transperfect.wd5.myworkdayjobs.com/transperfect
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import requests

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)


session = requests.Session()
ROMANIA_LOCATION_ID = "04de9d10ef0101e811e2f443bc2ba9f3"
CAREERS_URL = (
    "https://transperfect.wd5.myworkdayjobs.com/transperfect"
    f"?locations={ROMANIA_LOCATION_ID}"
)
API_URL = "https://transperfect.wd5.myworkdayjobs.com/wday/cxs/transperfect/transperfect/jobs"


def get_headers():
    '''
    ... initialize session and build Workday headers.
    '''
    session.get(CAREERS_URL, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
    csrf_token = session.cookies.get('CALYPSO_CSRF_TOKEN', '')

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://transperfect.wd5.myworkdayjobs.com',
        'Referer': CAREERS_URL,
        'User-Agent': 'Mozilla/5.0',
    }
    if csrf_token:
        headers['X-CALYPSO-CSRF-TOKEN'] = csrf_token

    return headers


def get_location_data(location_text):
    '''
    ... normalize Workday Romania location.
    '''
    city = location_text.split('-')[-1].replace('+', '').strip()
    if city == 'Bucharest':
        city = 'Bucuresti'

    county_data = get_county(location=city)
    county = county_data[0] if True in county_data else ''

    return county, city


def scraper():
    '''
    ... scrape data from TransPerfect scraper.
    '''
    payload = {
        'appliedFacets': {
            'locations': [ROMANIA_LOCATION_ID],
        },
        'limit': 20,
        'offset': 0,
        'searchText': '',
    }
    response = session.post(API_URL, headers=get_headers(), json=payload, timeout=30).json()

    job_list = []
    for job in response.get('jobPostings') or []:
        county, city = get_location_data(job.get('locationsText', 'Romania'))

        job_list.append(Item(
            job_title=job.get('title'),
            job_link='https://transperfect.wd5.myworkdayjobs.com/en-US/transperfect' + job.get('externalPath', ''),
            company='TransPerfect',
            country='Romania',
            county=county,
            city=city,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "TransPerfect"
    logo_link = "https://em-tti.eu/wp-content/uploads/2018/12/TP_Stacked_CMYK.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
