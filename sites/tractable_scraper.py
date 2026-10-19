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


def get_postal_address(job):
    '''
    ... postal address from the Ashby payload.
    '''
    return ((job.get('address') or {}).get('postalAddress')) or {}


def is_romania_job(job):
    '''
    ... check every location the job is published for (primary, secondary and
    postal address) to see if it is a Romania based job.
    '''
    address = get_postal_address(job)

    searchable_locations = ' '.join(
        [job.get('location') or '']
        + [str(item) for item in job.get('secondaryLocations') or []]
        + [
            str(address.get(field) or '')
            for field in ('addressCountry', 'addressRegion', 'addressLocality')
        ]
    ).lower()

    return 'romania' in searchable_locations or 'bucharest' in searchable_locations


def scraper():
    '''
    ... scrape data from Tractable scraper.
    '''
    jobs_data = GetRequestJson("https://api.ashbyhq.com/posting-api/job-board/tractable")

    jobs = jobs_data.get('jobs') or []
    romania_jobs = [job for job in jobs if is_romania_job(job)]

    # the job board has no Romania jobs left -> take the full list
    job_list = []
    for job in (romania_jobs or jobs):
        location = job.get('location') or ''
        address = get_postal_address(job)

        city = location.split(',')[0].strip() if location else ''
        if city.lower() == 'bucharest':
            county = 'Bucuresti'
            city = 'Bucuresti'
        else:
            county = ''

        if not city:
            city = address.get('addressLocality') or ''

        job_list.append(Item(
            job_title=job.get('title'),
            job_link=job.get('jobUrl'),
            company='Tractable',
            country='Romania' if is_romania_job(job) else address.get('addressCountry') or 'Romania',
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
