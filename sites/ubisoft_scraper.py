#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Ubisoft
# Link ------> https://www.ubisoft.com/en-us/company/careers/search?countries=ro
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
    get_county,
    Item,
    UpdateAPI,
)

import requests


ALGOLIA_URL = 'https://avcvysejs1-dsn.algolia.net/1/indexes/*/queries'
ALGOLIA_PARAMS = {
    'x-algolia-agent': 'Algolia for JavaScript (4.8.4); Browser (lite); JS Helper (3.11.0); react (16.12.0); react-instantsearch (6.8.3)',
    'x-algolia-api-key': '7d1048c332e18838e52ed9d41a50ac7b',
    'x-algolia-application-id': 'AVCVYSEJS1',
}
ALGOLIA_HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Origin': 'https://www.ubisoft.com',
    'Referer': 'https://www.ubisoft.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def get_jobs_data():
    '''
    ... fetch Romania jobs from Ubisoft Algolia index.
    '''
    payload = {
        'requests': [
            {
                'indexName': 'jobs_en-us_default',
                'params': (
                    'facetFilters=%5B%5B%22countryCode%3Aro%22%5D%5D&'
                    'facets=%5B%22jobFamily%22%2C%22team%22%2C%22countryCode%22%2C%22cities%22%2C'
                    '%22contractType%22%2C%22workFlexibility%22%2C%22graduateProgram%22%5D&'
                    'highlightPostTag=%3C%2Fais-highlight-0000000000%3E&'
                    'highlightPreTag=%3Cais-highlight-0000000000%3E&'
                    'maxValuesPerFacet=100&page=0&query=&tagFilters='
                ),
            }
        ]
    }

    response = requests.post(
        ALGOLIA_URL,
        params=ALGOLIA_PARAMS,
        headers=ALGOLIA_HEADERS,
        json=payload,
        timeout=30,
    ).json()

    return response['results'][0]['hits']


def get_location_data(city):
    '''
    ... normalize Ubisoft city/county.
    '''
    if city == 'Bucharest':
        city = 'Bucuresti'

    county_data = get_county(location=city)
    county = county_data[0] if True in county_data else ''

    return county, city


def scraper():
    '''
    ... scrape data from Ubisoft scraper.
    '''
    job_list = []
    for job in get_jobs_data():
        county, city = get_location_data(job.get('city', 'Romania'))

        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('link'),
            company='Ubisoft',
            country='Romania',
            county=county,
            city=city,
            remote='on-site' if job.get('workFlexibility') == 'Office-based' else 'hybrid',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ubisoft"
    logo_link = "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc1/56be0df1e4b043c434798ee2/huge?r=s3&_1499175978307"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
