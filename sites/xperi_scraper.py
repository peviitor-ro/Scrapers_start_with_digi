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
# Company ---> Xperi
# Link ------> https://jobs.jobvite.com/xperi/jobs
#
# Note ---> Xperi has no jobs in Romania at the moment, so the full job list is
#           scraped and each job keeps the country from its JobPosting data.
#
import json

from __utils import (
    GetStaticSoup,
    get_county,
    Item,
    UpdateAPI,
)

BASE_URL = "https://jobs.jobvite.com"
JOBS_URL = "https://jobs.jobvite.com/xperi/jobs"


def get_locations(job_data):
    '''
    ... normalize the JobPosting jobLocation field into a list of locations.
    '''
    raw_locations = job_data.get('jobLocation')
    if not raw_locations:
        return []

    if isinstance(raw_locations, dict):
        raw_locations = [raw_locations]

    locations = []
    for raw_location in raw_locations:
        address = raw_location.get('address') or {}
        locations.append({
            'city': (address.get('addressLocality') or '').strip(),
            'county': (address.get('addressRegion') or '').strip(),
            'country': (address.get('addressCountry') or '').strip(),
        })

    return locations


def get_remote_type(job_data):
    '''
    ... normalize the JobPosting remote type.
    '''
    if str(job_data.get('jobLocationType') or '').upper() == 'TELECOMMUTE':
        return 'remote'

    return 'on-site'


def get_job_data(job_link):
    '''
    ... return the JobPosting JSON-LD object for a job detail page.
    '''
    detail_soup = GetStaticSoup(job_link)
    script = detail_soup.find('script', type='application/ld+json')
    if script is None or not script.string:
        return None

    try:
        job_data = json.loads(script.string)
    except (TypeError, ValueError):
        return None

    if isinstance(job_data, list):
        job_data = next(
            (item for item in job_data
             if isinstance(item, dict) and item.get('@type') == 'JobPosting'),
            None,
        )

    return job_data if isinstance(job_data, dict) else None


def scraper():
    '''
    ... scrape data from Xperi scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    seen_links = set()

    for anchor in soup.select('a.flex-row'):
        href = anchor.get('href')
        if not href:
            continue

        job_link = href if href.startswith('http') else BASE_URL + href
        if job_link in seen_links:
            continue
        seen_links.add(job_link)

        job_data = get_job_data(job_link)
        if job_data is None:
            continue

        locations = get_locations(job_data)
        remote = get_remote_type(job_data)

        if locations:
            country = locations[0]['country']
            city = locations[0]['city'] or locations[0]['county'] or country
            county = ''
            if country.lower() == 'romania':
                location_finish = get_county(location=city)
                county = location_finish[0] if True in location_finish else ''
        else:
            country = ''
            city = ''
            county = ''

        title_tag = anchor.select_one('.jv-job-list-name')
        job_title = job_data.get('title') or (
            title_tag.get_text(' ', strip=True) if title_tag else ''
        )

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='xperi',
            country=country,
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "xperi"
    logo_link = "https://mms.businesswire.com/media/20180104005277/en/632823/23/xpe_logo_rgb_201.jpg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
