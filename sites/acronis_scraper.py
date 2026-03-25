#
#
# Config for Dynamic Get Method -> For embedded JSON state.
#
# Company ---> Acronis
# Link ------> https://www.acronis.com/en-eu/careers/jobs/
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
import json

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)


def get_embedded_state():
    '''
    ... return embedded app state from Acronis careers page.
    '''
    soup = GetStaticSoup("https://www.acronis.com/en-eu/careers/jobs/")
    script_tag = soup.find('script', attrs={'id': 'app-state'})

    if script_tag is None or not script_tag.text.strip():
        return {}

    return json.loads(script_tag.text)


def get_location_data(location_name):
    '''
    ... normalize county and city from Acronis location.
    '''
    if location_name.lower() == 'romania':
        return '', ''

    if location_name.lower() == 'bucharest':
        location_name = 'Bucuresti'

    location_finish = get_county(location=location_name)

    return (
        location_finish[0] if True in location_finish else '',
        'all' if True in location_finish and location_name.lower() == location_finish[0].lower()
        and location_name.lower() != 'bucuresti' else location_name,
    )


def get_remote_type(job, matched_location):
    '''
    ... return remote type exactly from the location data exposed on site.
    '''
    matched_descriptor = (matched_location or {}).get('descriptor', '')
    primary_location = job.get('primaryLocation') or {}
    primary_descriptor = primary_location.get('descriptor', '')

    if 'remote' in matched_descriptor.lower():
        return 'remote'

    if matched_descriptor.lower() == 'romania' and 'remote' in primary_descriptor.lower():
        return 'remote'

    return 'on-site'


def scraper():
    '''
    ... scrape data from Acronis scraper.
    '''
    state_data = get_embedded_state()
    workday_jobs = state_data.get('workday', {}).get('items', [])

    job_list = []
    for job in workday_jobs:
        additional_locations = job.get('additionalLocations') or []

        for location in additional_locations:
            descriptor = (location or {}).get('descriptor', '')
            country_data = (location or {}).get('country') or {}
            country_name = country_data.get('descriptor', '')

            if 'romania' not in descriptor.lower() and 'romania' not in country_name.lower():
                continue

            location_name = descriptor.split(' - ')[0]
            county, city = get_location_data(location_name)
            remote = get_remote_type(job, location)

            job_list.append(Item(
                job_title=job.get('title'),
                job_link=job.get('url'),
                company='Acronis',
                country='Romania',
                county=county,
                city=city,
                remote=remote,
            ).to_dict())
            break

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Acronis"
    logo_link = "https://staticfiles.acronis.com/images/content/28234cac9b11c6179ff6460d2f01b448.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
