#
#
# Config for Dynamic Get Method -> For Json format!
#
# Company ---> Tractable
# Link ------> https://jobs.ashbyhq.com/tractable
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
    Item,
    UpdateAPI,
)


def get_remote_type(job):
    '''
    ... normalize remote type from Ashby payload.
    '''
    workplace_type = (job.get('workplaceType') or '').lower()

    if workplace_type == 'hybrid':
        return 'hybrid'

    if job.get('isRemote'):
        return 'remote'

    return 'on-site'


def scraper():
    '''
    ... scrape data from Tractable scraper.
    '''
    jobs_data = GetRequestJson("https://api.ashbyhq.com/posting-api/job-board/tractable")

    job_list = []
    for job in jobs_data.get('jobs') or []:
        location = job.get('location') or ''
        secondary_locations = job.get('secondaryLocations') or []

        searchable_locations = ' '.join(
            [location] + [str(item) for item in secondary_locations]
        ).lower()
        if 'romania' not in searchable_locations and 'bucharest' not in searchable_locations:
            continue

        city = location.split(',')[0].strip() if location else 'Romania'
        county = 'Bucuresti' if city.lower() == 'bucharest' else ''
        city = 'Bucuresti' if city.lower() == 'bucharest' else city

        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('jobUrl'),
            company='Tractable',
            country='Romania',
            county=county,
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

    company_name = "Tractable"
    logo_link = "https://media.graphassets.com/resize=w:1616,h:535,fit:crop/auto_image/compress/Q1HdbVpoSdnYkE3bf03V"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
