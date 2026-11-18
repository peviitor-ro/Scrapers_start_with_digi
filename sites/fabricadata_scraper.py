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
# Company ---> Fabric
# Link ------> https://ats.rippling.com/fabric-inc/jobs
#
#
import json

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def _extract_job_items(data):
    queries = (
        data.get('props', {})
        .get('pageProps', {})
        .get('dehydratedState', {})
        .get('queries', [])
    )
    for query in queries:
        key = query.get('queryKey') or []
        if isinstance(key, list) and key and key[0] == 'board' and 'job-posts' in key:
            state_data = query.get('state', {}).get('data') or {}
            if isinstance(state_data, dict):
                return state_data.get('items') or []
    return []


def _location_is_romania(location):
    if not isinstance(location, dict):
        return False
    country = str(
        location.get('country')
        or location.get('countryName')
        or location.get('countryCode')
        or ''
    ).lower()
    text = ' '.join(
        str(location.get(k) or '')
        for k in ('name', 'city', 'state', 'region', 'country', 'countryName')
    ).lower()
    return 'romania' in country or 'romania' in text


def _city_from_locations(locations):
    for location in locations:
        if not _location_is_romania(location):
            continue
        city = (
            location.get('city')
            or location.get('name')
            or location.get('label')
            or ''
        )
        if isinstance(city, str) and city.strip():
            city = city.strip()
            if city.lower() == 'bucharest':
                city = 'Bucuresti'
            return city
    return ''


def _remote_from_job(job):
    workplace = str(job.get('workplaceType') or job.get('workplace_type') or '').upper()
    if workplace == 'REMOTE':
        return 'remote'
    if workplace == 'HYBRID':
        return 'hybrid'
    return 'on-site'


def scraper():
    '''
    ... scrape data from Fabric scraper.
    '''
    careers_url = "https://ats.rippling.com/fabric-inc/jobs"
    soup = GetStaticSoup(careers_url)

    job_list = []

    script = soup.find('script', attrs={'id': '__NEXT_DATA__'})
    if not script or not script.string:
        return job_list

    try:
        data = json.loads(script.string)
    except Exception:
        return job_list

    for job in _extract_job_items(data):
        if not isinstance(job, dict):
            continue

        locations = job.get('workLocations') or job.get('locations') or job.get('jobLocations') or []
        if not any(_location_is_romania(loc) for loc in locations):
            continue

        job_title = (job.get('name') or job.get('title') or '').strip()
        if not job_title:
            continue

        job_id = job.get('uuid') or job.get('id') or job.get('slug') or ''
        job_link = job.get('url') or job.get('jobUrl') or job.get('applyUrl') or ''
        if job_link and job_link.startswith('/'):
            job_link = 'https://ats.rippling.com' + job_link
        if not job_link and job_id:
            job_link = f"https://ats.rippling.com/fabric-inc/jobs/{job_id}"
        if not job_link:
            job_link = careers_url

        city = _city_from_locations(locations)
        if not city:
            # fallback: try to read a plain location string
            for loc in locations:
                if _location_is_romania(loc):
                    loc_name = str(loc.get('name') or '')
                    if loc_name:
                        city = loc_name.split(',')[0].strip()

        location_finish = get_county(city) if city else (None, None)

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Fabric',
            country='Romania',
            county=location_finish[0] if True in location_finish else None,
            city=city if city else 'all',
            remote=_remote_from_job(job),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Fabric"
    logo_link = "https://mma.prnewswire.com/media/1701193/Fabric2_Logo.jpg?p=twitter"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
