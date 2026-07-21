#
#
# Config for Workday API -> For Json format!
#
# Company ---> BlackLine
# Link ------> https://careers.blackline.com/careers-home/jobs
#
#
from __utils import (
    get_county,
    Item,
    UpdateAPI,
)
import requests


WORKDAY_BASE = 'https://blackline.wd108.myworkdayjobs.com'
WORKDAY_CXS = '/wday/cxs/blackline/BlackLineCareers'
CAREERS_URL = 'https://careers.blackline.com/careers-home/jobs?page=2&location=Romania&woe=12&stretchUnit=MILES&stretch=10'

BUCHAREST_FACET_IDS = [
    '9574f3b33005100115a8fa1088a30000',
    'b14bb3de74cd1000ac19826a86a00000',
]


def init_session():
    '''
    ... init session and get cookies from site
    '''
    sess = requests.Session()
    sess.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    })
    sess.get(CAREERS_URL, verify=False)
    return sess


def scraper():
    '''
    ... scrape data from BlackLine scraper.
    '''
    sess = init_session()
    job_list = list()
    offset = 0
    limit = 20

    while True:
        payload = {
            'appliedFacets': {'locations': BUCHAREST_FACET_IDS},
            'limit': limit,
            'offset': offset,
            'searchText': '',
        }
        resp = sess.post(
            WORKDAY_BASE + WORKDAY_CXS + '/jobs',
            json=payload,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            verify=False,
        )
        data = resp.json()
        postings = data.get('jobPostings', [])

        if not postings:
            break

        for jp in postings:
            path = jp.get('externalPath', '')
            detail_resp = sess.get(
                WORKDAY_BASE + WORKDAY_CXS + path,
                headers={'Accept': 'application/json'},
                verify=False,
            )
            detail = detail_resp.json().get('jobPostingInfo', {})

            location = detail.get('location', 'Bucharest')
            remote_type = (detail.get('remoteType') or '').lower()

            if remote_type == 'remote':
                job_type = 'remote'
            elif remote_type == 'hybrid':
                job_type = 'hybrid'
            else:
                job_type = 'on-site'

            location_finish = get_county(location=location)

            job_list.append(Item(
                job_title=detail.get('title', jp.get('title', '')),
                job_link=WORKDAY_BASE + path,
                company='BlackLine',
                country='Romania',
                county=location_finish[0] if True in location_finish else None,
                city='all' if location.lower() == location_finish[0].lower()
                    and True in location_finish and 'bucuresti' != location.lower()
                    else location,
                remote=job_type,
            ).to_dict())

        offset += limit
        if offset >= data.get('total', 0):
            break

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "BlackLine"
    logo_link = "https://cms.jibecdn.com/prod/blackline/assets/HEADER-NAV_LOGO-en-us-1640926577769.svg"

    jobs = scraper()
    print(jobs, len(jobs))
    # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
