#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> Verifone
# Link ------> https://job-boards.greenhouse.io/verifone
#
#
import requests

from __utils import (
    get_county,
    Item,
    UpdateAPI,
)

GREENHOUSE_JOBS_URL = 'https://boards-api.greenhouse.io/v1/boards/verifone/jobs'


def scraper():
    '''
    ... scrape data from Verifone scraper.
    '''
    try:
        response = requests.get(
            GREENHOUSE_JOBS_URL,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=30,
        )
        response.raise_for_status()
        all_jobs = response.json().get('jobs', [])
    except (requests.exceptions.ConnectTimeout, requests.exceptions.Timeout,
            requests.exceptions.ConnectionError, ValueError):
        return []

    job_list = []
    for job in all_jobs:
        location_name = job.get('location', {}).get('name', '') or ''
        romania_location = next(
            (part.strip() for part in location_name.split(';')
             if 'romania' in part.lower() or 'bucharest' in part.lower()),
            None,
        )
        if romania_location is None:
            continue

        city = romania_location.split(',')[0].strip()
        normalized_city = 'Bucuresti' if city.lower() == 'bucharest' else city
        county_data = get_county(location=normalized_city)

        job_list.append(Item(
            job_title=job.get('title', '').strip(),
            job_link=(job.get('absolute_url') or '').strip(),
            company='Verifone',
            country='Romania',
            county=county_data[0] if True in county_data else '',
            city=normalized_city,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Verifone"
    logo_link = "https://datasym.co.uk/wp-content/uploads/2017/09/verifone-logo-300x120.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
