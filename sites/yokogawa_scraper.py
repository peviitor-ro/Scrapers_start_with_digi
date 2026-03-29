#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Yokogawa
# Link ------> https://wd3.myworkdaysite.com/recruiting/yokogawa/yokogawa-career-site
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

from __utils import Item, UpdateAPI


session = requests.Session()
ROMANIA_LOCATION_ID = 'f2e609fe92974a55a05fc1cdc2852122'
CAREERS_URL = 'https://wd3.myworkdaysite.com/recruiting/yokogawa/yokogawa-career-site'
API_URL = 'https://wd3.myworkdaysite.com/wday/cxs/yokogawa/yokogawa-career-site/jobs'


def get_headers():
    '''
    ... initialize session and build Workday headers.
    '''
    session.get(CAREERS_URL, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
    csrf_token = session.cookies.get('CALYPSO_CSRF_TOKEN', '')

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://wd3.myworkdaysite.com',
        'Referer': CAREERS_URL,
        'User-Agent': 'Mozilla/5.0',
    }
    if csrf_token:
        headers['X-CALYPSO-CSRF-TOKEN'] = csrf_token

    return headers


def get_remote_type(job):
    '''
    ... normalize Workday remote type.
    '''
    remote_type = (job.get('remoteType') or '').lower()
    if 'hybrid' in remote_type:
        return 'hybrid'
    if 'remote' in remote_type:
        return 'remote'
    return 'on-site'


def scraper():
    '''
    ... scrape data from Yokogawa scraper.
    '''
    payload = {
        'appliedFacets': {
            'locationCountry': [ROMANIA_LOCATION_ID],
        },
        'searchText': '',
    }
    response = session.post(API_URL, headers=get_headers(), json=payload, timeout=30).json()

    job_list = []
    for job in response.get('jobPostings') or []:
        city = 'Bucuresti'

        job_list.append(Item(
            job_title=job.get('title') or '',
            job_link=(
                'https://wd3.myworkdaysite.com/en-US/recruiting/yokogawa/'
                f'yokogawa-career-site{job.get("externalPath", "")}?locationCountry={ROMANIA_LOCATION_ID}'
            ),
            company='yokogawa',
            country='Romania',
            county='Bucuresti',
            city=city,
            remote=get_remote_type(job),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = 'yokogawa'
    logo_link = 'https://web-material3.yokogawa.com/1/10029/tabs/trademark.jpg'

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
