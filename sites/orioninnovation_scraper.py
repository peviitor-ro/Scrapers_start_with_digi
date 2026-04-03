from __utils import (
    Item,
    get_county,
    UpdateAPI
)

import requests


def scraper():
    '''
    ... scrape data from OrionInnovation using Greenhouse API.
    '''
    response = requests.get(
        'https://boards-api.greenhouse.io/v1/boards/orioninnovation/jobs?content=true',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    all_jobs = response.json().get('jobs', [])

    job_list = []
    for job in all_jobs:
        location_name = job.get('location', {}).get('name', '').lower()
        if 'romania' not in location_name and 'bucharest' not in location_name:
            continue

        title = job.get('title', '')
        job_link = job.get('absolute_url', '')
        job_type = 'remote' if 'remote' in title.lower() else 'hybrid'

        if 'bucharest' in location_name:
            city = 'Bucuresti'
        else:
            city = location_name.title()

        location_finish = get_county(location=city)
        job_list.append(Item(
            job_title=title,
            job_link=job_link,
            company='OrionInnovation',
            country='Romania',
            county=location_finish[0] if True in location_finish else '',
            city=city,
            remote=job_type,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "OrionInnovation"
    logo_link = "https://www.orioninnovation.com/wp-content/uploads/2022/08/Orion-Innovation-Logo-1.png"

    jobs = scraper()
    print(f"Found {len(jobs)} jobs in Romania")

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
